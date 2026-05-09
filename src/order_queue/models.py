"""
队列数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any


class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"           # 等待打印
    PRINTED = "printed"           # 已打印，制作中
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"             # 打印失败
    FALLBACK = "fallback"         # 已回退到原始模式


class DrinkType(Enum):
    """饮品类型"""
    HOT = "hot"
    COLD = "cold"


@dataclass
class DrinkStep:
    """制作步骤"""
    sequence: int          # 步骤序号
    description: str       # 步骤描述
    completed: bool = False  # 是否完成


@dataclass
class DrinkOrder:
    """单杯饮品订单"""
    # 标识信息
    order_id: str                      # 原始订单号
    drink_id: str                      # 饮品唯一ID
    sequence: int                      # 当前是第几杯
    total: int                         # 总共几杯
    
    # 饮品信息
    drink_name: str                    # 饮品名称
    drink_type: DrinkType              # 热/冷
    specs: Dict[str, Any] = field(default_factory=dict)  # 规格
    
    # 制作信息
    steps: List[DrinkStep] = field(default_factory=list)
    notes: str = ""                    # 备注
    
    # 状态信息
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    printed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # 原始数据（用于回退）
    raw_order: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "order_id": self.order_id,
            "drink_id": self.drink_id,
            "sequence": self.sequence,
            "total": self.total,
            "drink_name": self.drink_name,
            "status": self.status.value,
            "steps": [s.description for s in self.steps],
            "created_at": self.created_at.isoformat()
        }


@dataclass
class OrderBatch:
    """订单批次（一个外卖订单可能包含多杯）"""
    batch_id: str                      # 批次ID
    source: str                        # 来源（美团/饿了么/线下）
    orders: List[DrinkOrder] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
