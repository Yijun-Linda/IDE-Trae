# AI认知翻译官 - Webhook接收模块
"""
提供外卖平台订单接收功能。
"""

from .handler import create_app, init_queue

__all__ = [
    "create_app",
    "init_queue",
]
