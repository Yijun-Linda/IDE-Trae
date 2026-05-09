"""
队列管理器
"""

import threading
import time
import logging
from typing import List, Optional, Callable
from datetime import datetime

from .models import DrinkOrder, OrderStatus, DrinkStep

logger = logging.getLogger(__name__)


class QueueFullError(Exception):
    """队列已满异常"""
    pass


class PrintQueue:
    """打印队列管理器"""
    
    def __init__(
        self,
        translator,           # 翻译引擎
        printer,              # 打印机
        delay_minutes: int = 5,
        max_size: int = 20
    ):
        """
        初始化队列管理器
        
        Args:
            translator: 翻译引擎实例
            printer: 打印机实例
            delay_minutes: 每杯制作间隔（分钟）
            max_size: 最大队列长度
        """
        self.translator = translator
        self.printer = printer
        self.delay_minutes = delay_minutes
        self.max_size = max_size
        
        # 队列存储
        self._queue: List[DrinkOrder] = []
        self._current_index: int = 0
        self._lock = threading.Lock()
        
        # 调度器
        self._timers: List[threading.Timer] = []
        self._running = False
        
        # 回调函数
        self.on_print: Optional[Callable] = None
        self.on_complete: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
    
    def start(self):
        """启动队列管理器"""
        self._running = True
        logger.info("Print queue started")
    
    def stop(self):
        """停止队列管理器"""
        self._running = False
        # 取消所有定时器
        for timer in self._timers:
            timer.cancel()
        self._timers.clear()
        logger.info("Print queue stopped")
    
    def add_batch(self, raw_order: dict) -> List[str]:
        """
        添加新订单批次
        
        Args:
            raw_order: 原始订单数据
            
        Returns:
            生成的drink_id列表
            
        Raises:
            QueueFullError: 队列已满
        """
        with self._lock:
            # 检查队列长度
            if len(self._queue) >= self.max_size:
                raise QueueFullError(f"Queue is full (max {self.max_size})")
            
            # 解析订单
            orders = self._parse_order(raw_order)
            
            # 添加到队列
            start_index = len(self._queue)
            self._queue.extend(orders)
            
            logger.info(f"Added {len(orders)} orders to queue. Total: {len(self._queue)}")
            
            # 如果是第一杯，立即打印
            if start_index == 0 and self._current_index == 0:
                self._print_current()
            
            return [o.drink_id for o in orders]
    
    def _parse_order(self, raw_order: dict) -> List[DrinkOrder]:
        """
        解析原始订单为多杯饮品
        
        Args:
            raw_order: 原始订单数据
            
        Returns:
            饮品订单列表
        """
        orders = []
        order_id = raw_order.get("order_id", f"ORD{int(time.time())}")
        items = raw_order.get("items", [])
        
        # 计算总杯数
        total_cups = sum(item.get("quantity", 1) for item in items)
        
        sequence = 1
        for item in items:
            quantity = item.get("quantity", 1)
            
            for i in range(quantity):
                # 调用AI翻译
                order_text = f"{item.get('name', '未知饮品')}({item.get('specs', '')})"
                translation = self.translator.translate(order_text)
                
                if translation.get("success"):
                    # 创建步骤
                    steps = [
                        DrinkStep(seq, desc)
                        for seq, desc in enumerate(translation["steps"], 1)
                    ]
                    
                    # 判断饮品类型
                    drink_name = translation["drink_name"]
                    from .models import DrinkType
                    drink_type = DrinkType.COLD if "冰" in drink_name else DrinkType.HOT
                    
                    order = DrinkOrder(
                        order_id=order_id,
                        drink_id=f"{order_id}_{sequence}",
                        sequence=sequence,
                        total=total_cups,
                        drink_name=drink_name,
                        drink_type=drink_type,
                        steps=steps,
                        notes=translation.get("notes", ""),
                        raw_order=raw_order
                    )
                else:
                    # 翻译失败，创建回退订单
                    order = self._create_fallback_order(
                        order_id, sequence, total_cups, item, raw_order
                    )
                
                orders.append(order)
                sequence += 1
        
        return orders
    
    def _create_fallback_order(
        self,
        order_id: str,
        sequence: int,
        total: int,
        item: dict,
        raw_order: dict
    ) -> DrinkOrder:
        """
        创建回退订单（AI翻译失败时使用）
        
        Args:
            order_id: 订单号
            sequence: 序号
            total: 总数
            item: 商品信息
            raw_order: 原始订单
            
        Returns:
            回退订单
        """
        from .models import DrinkType
        
        return DrinkOrder(
            order_id=order_id,
            drink_id=f"{order_id}_{sequence}",
            sequence=sequence,
            total=total,
            drink_name=item.get("name", "未知饮品"),
            drink_type=DrinkType.HOT,
            steps=[DrinkStep(1, "请杨老师协助")],
            notes="AI翻译失败",
            status=OrderStatus.FALLBACK,
            raw_order=raw_order
        )
    
    def _print_current(self):
        """打印当前杯"""
        with self._lock:
            if self._current_index >= len(self._queue):
                return
            
            order = self._queue[self._current_index]
            
            try:
                # 渲染小票
                from ..printer.template import TicketTemplate, TicketData
                
                template = TicketTemplate()
                data = TicketData(
                    order_id=order.order_id,
                    current=order.sequence,
                    total=order.total,
                    drink_name=order.drink_name,
                    steps=[s.description for s in order.steps],
                    notes=order.notes,
                    delay_minutes=self.delay_minutes
                )
                
                content = template.render(data)
                
                # 打印
                result = self.printer.print_ticket(content)
                
                if result["success"]:
                    order.status = OrderStatus.PRINTED
                    order.printed_at = datetime.now()
                    logger.info(f"Printed order {order.drink_id}")
                    
                    # 触发回调
                    if self.on_print:
                        self.on_print(order)
                    
                    # 调度下一杯
                    self._schedule_next()
                else:
                    order.status = OrderStatus.FAILED
                    logger.error(f"Failed to print {order.drink_id}: {result['message']}")
                    
                    if self.on_error:
                        self.on_error(order, result["message"])
                
            except Exception as e:
                logger.error(f"Exception printing {order.drink_id}: {e}", exc_info=True)
                order.status = OrderStatus.FAILED
                
                if self.on_error:
                    self.on_error(order, str(e))
    
    def _schedule_next(self):
        """调度下一杯"""
        next_index = self._current_index + 1
        
        if next_index >= len(self._queue):
            logger.info("All orders completed")
            return
        
        delay_seconds = self.delay_minutes * 60
        
        logger.info(f"Scheduling next order in {self.delay_minutes} minutes")
        
        timer = threading.Timer(delay_seconds, self._on_delay_complete)
        timer.start()
        self._timers.append(timer)
    
    def _on_delay_complete(self):
        """延迟完成回调"""
        with self._lock:
            # 标记当前杯完成
            if self._current_index < len(self._queue):
                current = self._queue[self._current_index]
                current.status = OrderStatus.COMPLETED
                current.completed_at = datetime.now()
                
                logger.info(f"Completed order {current.drink_id}")
                
                if self.on_complete:
                    self.on_complete(current)
            
            # 移动到下一杯
            self._current_index += 1
            
            # 打印下一杯
            if self._current_index < len(self._queue):
                self._print_current()
    
    def get_status(self) -> dict:
        """
        获取队列状态
        
        Returns:
            队列状态字典
        """
        with self._lock:
            return {
                "total_orders": len(self._queue),
                "current_index": self._current_index + 1,
                "pending": len([o for o in self._queue if o.status == OrderStatus.PENDING]),
                "printed": len([o for o in self._queue if o.status == OrderStatus.PRINTED]),
                "completed": len([o for o in self._queue if o.status == OrderStatus.COMPLETED]),
                "failed": len([o for o in self._queue if o.status == OrderStatus.FAILED]),
                "is_running": self._running
            }
    
    def get_current_order(self) -> Optional[DrinkOrder]:
        """
        获取当前正在制作的订单
        
        Returns:
            当前订单或None
        """
        with self._lock:
            if self._current_index < len(self._queue):
                return self._queue[self._current_index]
            return None
    
    def skip_current(self):
        """跳过当前杯（人工干预）"""
        with self._lock:
            if self._current_index < len(self._queue):
                current = self._queue[self._current_index]
                current.status = OrderStatus.COMPLETED
                current.completed_at = datetime.now()
                
                # 取消当前定时器
                for timer in self._timers:
                    timer.cancel()
                self._timers.clear()
                
                # 移动到下一杯并立即打印
                self._current_index += 1
                if self._current_index < len(self._queue):
                    self._print_current()
