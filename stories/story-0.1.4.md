# Story-0.1.4: 时间延迟自动出单实现

## 关联信息
- 所属版本：v0.1
- 关联文档：mvp.md#1.3 产品形态、mvp.md#四、设计原则
- 前置依赖：story-0.1.1（打印机API）、story-0.1.2（翻译引擎）、story-0.1.3（小票模板）
- 优先级：P0

## 任务描述

实现打印队列管理和时间延迟自动出单机制。员工完成一杯后，系统等待5分钟，自动打印下一杯的指引小票。

### 核心机制
1. **队列管理**：接收订单后按杯数拆解，加入队列
2. **时间延迟**：每杯制作完成后等待固定时间（默认5分钟）
3. **自动出单**：时间到自动打印下一杯的小票
4. **异常回退**：AI服务异常时自动切换回原始小票模式

### 设计决策
- **为什么用时间延迟而非按钮？**
  - 比赛MVP简化设计，减少硬件依赖
  - 5分钟延迟基于新手拉花时间估算
  - 后续v1.0可升级为按钮控制

## 认知约束

### 工作记忆是稀缺资源
- 一次只处理一杯，避免认知超载
- 当前小票完成后，下一张才出现

### 被动接收优于主动检索
- 员工无需主动获取下一单
- 时间到自动出票，零操作成本

### 极限推演思维
- 边界条件：当订单量达到10杯时队列是否还能工作？
- 异常条件：当打印机卡纸时如何处理？
- 极端条件：当系统重启时队列状态如何恢复？

## 完成标准

### 功能标准
- [ ] 订单队列管理实现
- [ ] 时间延迟机制实现（默认5分钟，可配置）
- [ ] 自动出单触发逻辑
- [ ] 异常回退机制（AI失败时打印原始小票）

### 验证标准
- [ ] 时间延迟准确（5分钟±30秒）
- [ ] 队列管理无丢单、无重复
- [ ] 多订单场景测试通过（模拟10杯订单）
- [ ] 异常回退测试通过（断网、AI超时）
- [ ] 代码覆盖率 > 80%

### 文档标准
- [ ] 队列设计文档（docs/dev0.1/0.1.4-queue-management.md）
- [ ] 配置说明（延迟时间调整方法）
- [ ] 故障排查指南

## 相关文件

- 代码路径：src/queue/
  - `__init__.py`
  - `manager.py` - 队列管理器
  - `scheduler.py` - 定时调度器
  - `models.py` - 队列数据模型
- 代码路径：src/webhook/
  - `handler.py` - Webhook接收处理器
- 测试路径：tests/test_queue.py
- 文档路径：docs/dev0.1/0.1.4-queue-management.md

## 技术细节

### 队列数据模型

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"      # 等待中
    PRINTED = "printed"      # 已打印
    COMPLETED = "completed"  # 已完成（时间到）
    FAILED = "failed"        # 打印失败

@dataclass
class DrinkOrder:
    """单杯饮品订单"""
    order_id: str           # 原始订单号
    drink_id: str          # 饮品唯一ID（order_id + 序号）
    sequence: int          # 当前是第几杯
    total: int             # 总共几杯
    drink_name: str        # 饮品名称
    steps: list[str]       # 制作步骤
    status: OrderStatus
    created_at: datetime
    printed_at: datetime = None
    completed_at: datetime = None
```

### 队列管理器

```python
class PrintQueue:
    """打印队列管理器"""
    
    def __init__(self, delay_minutes: int = 5):
        self.delay_minutes = delay_minutes
        self.queue = []  # DrinkOrder列表
        self.current_index = 0
        self.scheduler = Scheduler()
    
    def add_order(self, raw_order: dict) -> list[str]:
        """
        添加新订单到队列
        
        Args:
            raw_order: 原始订单数据
            
        Returns:
            生成的drink_id列表
        """
        # 1. 拆解订单为多杯
        # 2. 调用AI翻译每杯
        # 3. 加入队列
        # 4. 如果是第一杯，立即打印
        pass
    
    def complete_current(self):
        """标记当前杯完成，调度下一杯"""
        if self.current_index < len(self.queue):
            current = self.queue[self.current_index]
            current.status = OrderStatus.COMPLETED
            current.completed_at = datetime.now()
            
            # 调度下一杯
            self.current_index += 1
            if self.current_index < len(self.queue):
                self.scheduler.schedule(
                    delay_seconds=self.delay_minutes * 60,
                    task=self._print_next
                )
    
    def _print_next(self):
        """打印下一杯"""
        if self.current_index < len(self.queue):
            order = self.queue[self.current_index]
            # 调用打印机API
            # 更新状态
            pass
    
    def get_status(self) -> dict:
        """获取队列状态"""
        return {
            "total": len(self.queue),
            "current": self.current_index + 1,
            "pending": len([o for o in self.queue if o.status == OrderStatus.PENDING]),
            "completed": len([o for o in self.queue if o.status == OrderStatus.COMPLETED])
        }
```

### 定时调度器

```python
import threading
import time
from typing import Callable

class Scheduler:
    """简单定时调度器（基于threading）"""
    
    def __init__(self):
        self.timers = []
    
    def schedule(self, delay_seconds: int, task: Callable):
        """
        调度一个延迟任务
        
        Args:
            delay_seconds: 延迟秒数
            task: 要执行的任务函数
        """
        timer = threading.Timer(delay_seconds, task)
        timer.start()
        self.timers.append(timer)
    
    def cancel_all(self):
        """取消所有待执行任务"""
        for timer in self.timers:
            timer.cancel()
        self.timers.clear()
```

### Webhook接收处理器

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
queue = PrintQueue(delay_minutes=5)

@app.route('/webhook/order', methods=['POST'])
def receive_order():
    """接收外卖平台订单"""
    try:
        raw_order = request.json
        
        # 验证订单签名（防止伪造）
        if not verify_signature(request):
            return jsonify({"error": "Invalid signature"}), 401
        
        # 添加到队列
        drink_ids = queue.add_order(raw_order)
        
        return jsonify({
            "success": True,
            "drink_ids": drink_ids,
            "queue_status": queue.get_status()
        })
    
    except Exception as e:
        # 异常时打印原始小票作为回退
        print_raw_ticket(raw_order)
        return jsonify({"error": str(e)}), 500

def verify_signature(request) -> bool:
    """验证Webhook签名"""
    # 实现签名验证逻辑
    pass

def print_raw_ticket(raw_order: dict):
    """打印原始小票（异常回退）"""
    # 直接打印原始订单内容
    pass
```

### 异常回退机制

```python
class FallbackHandler:
    """异常回退处理器"""
    
    def __init__(self, printer):
        self.printer = printer
    
    def handle_translation_error(self, raw_order: dict):
        """AI翻译失败时的回退"""
        # 格式化原始订单为简单文本
        content = self._format_raw_order(raw_order)
        self.printer.print_ticket(content)
    
    def _format_raw_order(self, raw_order: dict) -> str:
        """将原始订单格式化为可打印文本"""
        lines = []
        lines.append("=" * 16)
        lines.append("原始订单".center(16))
        lines.append("=" * 16)
        lines.append(f"订单号: {raw_order.get('order_id', 'N/A')}")
        lines.append("")
        
        for item in raw_order.get('items', []):
            lines.append(f"{item.get('name', '未知饮品')}")
            if item.get('specs'):
                lines.append(f"  {item.get('specs')}")
        
        lines.append("")
        lines.append("请杨老师协助处理".center(16))
        
        return "\n".join(lines)
```

## 状态
- [x] 待开始 / [ ] 进行中 / [ ] 已完成

## 备注

### 配置参数

| 参数名 | 默认值 | 说明 | 调整范围 |
|--------|--------|------|---------|
| DELAY_MINUTES | 5 | 每杯制作时间 | 3-10分钟 |
| MAX_QUEUE_SIZE | 20 | 最大队列长度 | 10-50 |
| RETRY_TIMES | 3 | 打印失败重试次数 | 1-5 |

### 风险与应对
| 风险 | 应对措施 |
|------|---------|
| 5分钟延迟不合理 | 实地测试后调整，可配置化 |
| 系统重启丢失队列 | 比赛阶段简化，不持久化；v1.0可加数据库 |
| 多订单同时涌入 | 队列长度限制，超限提醒杨老师 |
| 定时器精度问题 | 使用threading.Timer，精度足够 |

### 后续演进
- v1.0：无线按钮替代时间延迟，员工主动控制节奏
- v1.0：队列持久化，支持系统重启恢复
- v2.0：智能调度，根据饮品复杂度动态调整延迟
