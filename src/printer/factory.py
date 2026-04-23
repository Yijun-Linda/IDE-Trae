"""
打印机工厂
用于创建不同类型的打印机实例
"""

import logging
from typing import Dict, Any

from .base import BasePrinter
from .yilianyun import YilianyunPrinter
from .feie import FeiePrinter

logger = logging.getLogger(__name__)


class PrinterFactory:
    """打印机工厂类"""
    
    # 支持的打印机类型
    PROVIDERS = {
        "yilianyun": YilianyunPrinter,
        "feie": FeiePrinter,
    }
    
    @classmethod
    def create(cls, provider: str, config: Dict[str, Any]) -> BasePrinter:
        """
        创建打印机实例
        
        Args:
            provider: 打印机厂商类型 (yilianyun/feie)
            config: 打印机配置
            
        Returns:
            打印机实例
            
        Raises:
            ValueError: 不支持的厂商类型
        """
        provider = provider.lower()
        
        if provider not in cls.PROVIDERS:
            available = ", ".join(cls.PROVIDERS.keys())
            raise ValueError(
                f"Unknown printer provider: {provider}. "
                f"Available: {available}"
            )
        
        printer_class = cls.PROVIDERS[provider]
        logger.info(f"Creating printer instance: {provider}")
        
        return printer_class(config)
    
    @classmethod
    def create_from_env(cls, provider: str = None) -> BasePrinter:
        """
        从环境变量创建打印机实例
        
        Args:
            provider: 厂商类型，默认从环境变量读取
            
        Returns:
            打印机实例
        """
        import os
        
        provider = provider or os.getenv("PRINTER_PROVIDER", "yilianyun")
        
        if provider == "yilianyun":
            config = {
                "app_id": os.getenv("YILIANYUN_APP_ID"),
                "app_secret": os.getenv("YILIANYUN_APP_SECRET"),
                "machine_code": os.getenv("YILIANYUN_MACHINE_CODE"),
                "timeout": int(os.getenv("PRINTER_TIMEOUT", "10"))
            }
        elif provider == "feie":
            config = {
                "user": os.getenv("FEIE_USER"),
                "ukey": os.getenv("FEIE_UKEY"),
                "sn": os.getenv("FEIE_SN"),
                "timeout": int(os.getenv("PRINTER_TIMEOUT", "10"))
            }
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        # 验证必要配置
        missing = [k for k, v in config.items() if v is None and k != "timeout"]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
        
        return cls.create(provider, config)
    
    @classmethod
    def list_providers(cls) -> list:
        """
        列出支持的打印机厂商
        
        Returns:
            厂商列表
        """
        return list(cls.PROVIDERS.keys())
