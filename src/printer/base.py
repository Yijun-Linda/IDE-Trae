"""
打印机抽象基类
定义统一的打印机接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class BasePrinter(ABC):
    """打印机抽象基类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化打印机
        
        Args:
            config: 打印机配置字典
        """
        self.config = config
        self.timeout = config.get("timeout", 10)
        self.dry_run_mode = False
    
    @abstractmethod
    def print_ticket(self, content: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        打印小票
        
        Args:
            content: 打印内容（纯文本或ESC/POS指令）
            dry_run: 是否仅预览不实际打印
            
        Returns:
            {
                "success": bool,
                "order_id": str,      # 打印任务ID
                "message": str,       # 状态信息
                "preview": str        # dry_run时的预览内容
            }
        """
        pass
    
    @abstractmethod
    def query_status(self, order_id: str) -> Dict[str, Any]:
        """
        查询打印任务状态
        
        Args:
            order_id: 打印任务ID
            
        Returns:
            {
                "success": bool,
                "status": str,        # pending/printing/completed/failed
                "printed": bool,      # 是否已打印
                "message": str
            }
        """
        pass
    
    @abstractmethod
    def is_online(self) -> bool:
        """
        检查打印机是否在线
        
        Returns:
            是否在线
        """
        pass
    
    def validate_content(self, content: str) -> bool:
        """
        验证打印内容（通用检查）
        
        Args:
            content: 打印内容
            
        Returns:
            是否有效
        """
        if not content:
            logger.warning("Content is empty")
            return False
        
        if len(content) > 4096:  # 最大长度限制
            logger.warning(f"Content too long: {len(content)} chars")
            return False
        
        return True
    
    def set_dry_run(self, enabled: bool = True):
        """
        设置dry-run模式
        
        Args:
            enabled: 是否启用
        """
        self.dry_run_mode = enabled
        logger.info(f"Dry-run mode: {enabled}")
