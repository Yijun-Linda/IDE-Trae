# AI认知翻译官 - 翻译模块
"""
提供AI订单翻译功能，将咖啡订单翻译为可执行的动作脚本。
"""

from .translator import OrderTranslator, BatchTranslator
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, FEW_SHOT_EXAMPLES

__all__ = [
    "OrderTranslator",
    "BatchTranslator",
    "SYSTEM_PROMPT",
    "USER_PROMPT_TEMPLATE",
    "FEW_SHOT_EXAMPLES",
]
