"""
Webhook接收处理器
"""

import os
import hmac
import hashlib
import logging
from typing import Optional

from flask import Flask, request, jsonify

from ..queue.manager import PrintQueue, QueueFullError
from ..translator.translator import OrderTranslator
from ..printer.factory import PrinterFactory

logger = logging.getLogger(__name__)

# 全局队列实例
queue: Optional[PrintQueue] = None


def init_queue(translator, printer, config: dict):
    """
    初始化队列
    
    Args:
        translator: 翻译引擎
        printer: 打印机
        config: 配置字典
    """
    global queue
    queue = PrintQueue(
        translator=translator,
        printer=printer,
        delay_minutes=config.get("delay_minutes", 5),
        max_size=config.get("max_queue_size", 20)
    )
    queue.start()
    logger.info("Queue initialized and started")


def create_app() -> Flask:
    """
    创建Flask应用
    
    Returns:
        Flask应用实例
    """
    app = Flask(__name__)
    
    @app.route('/webhook/order', methods=['POST'])
    def receive_order():
        """接收外卖平台订单"""
        try:
            # 验证签名
            if not verify_signature(request):
                logger.warning("Invalid webhook signature")
                return jsonify({"error": "Invalid signature"}), 401
            
            # 解析订单
            raw_order = request.json
            logger.info(f"Received order: {raw_order.get('order_id')}")
            
            # 添加到队列
            drink_ids = queue.add_batch(raw_order)
            
            return jsonify({
                "success": True,
                "drink_ids": drink_ids,
                "queue_status": queue.get_status()
            })
        
        except QueueFullError as e:
            logger.error(f"Queue full: {e}")
            return jsonify({"error": "Queue is full", "message": str(e)}), 503
        
        except Exception as e:
            logger.error(f"Error processing order: {e}", exc_info=True)
            # 异常时打印原始小票作为回退
            try:
                print_raw_fallback(request.json)
            except:
                pass
            return jsonify({"error": str(e)}), 500
    
    @app.route('/queue/status', methods=['GET'])
    def get_queue_status():
        """获取队列状态"""
        if queue is None:
            return jsonify({"error": "Queue not initialized"}), 500
        
        return jsonify(queue.get_status())
    
    @app.route('/queue/skip', methods=['POST'])
    def skip_current():
        """跳过当前杯（人工干预）"""
        if queue is None:
            return jsonify({"error": "Queue not initialized"}), 500
        
        queue.skip_current()
        return jsonify({"success": True, "queue_status": queue.get_status()})
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """健康检查"""
        return jsonify({
            "status": "healthy",
            "queue_initialized": queue is not None
        })
    
    return app


def verify_signature(request) -> bool:
    """
    验证Webhook签名
    
    Args:
        request: Flask请求对象
        
    Returns:
        签名是否有效
    """
    secret = os.getenv("WEBHOOK_SECRET", "")
    if not secret:
        # 开发环境跳过验证
        return True
    
    signature = request.headers.get('X-Signature', '')
    body = request.get_data()
    
    expected = hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)


def print_raw_fallback(raw_order: dict):
    """
    打印原始小票（异常回退）
    
    Args:
        raw_order: 原始订单数据
    """
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
    lines.append("请杨老师协助".center(16))
    
    content = "\n".join(lines)
    
    # 发送到打印机
    if queue and queue.printer:
        queue.printer.print_ticket(content)


if __name__ == '__main__':
    # 初始化组件
    translator = OrderTranslator()
    printer = PrinterFactory.create_from_env()
    
    config = {
        "delay_minutes": int(os.getenv('DELAY_MINUTES', '5')),
        "max_queue_size": int(os.getenv('MAX_QUEUE_SIZE', '20'))
    }
    
    init_queue(translator, printer, config)
    
    # 启动应用
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
