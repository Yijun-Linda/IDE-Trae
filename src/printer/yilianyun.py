"""
易联云打印机实现
API文档: https://www.10ss.net/help.html
"""

import hashlib
import time
import logging
from typing import Dict, Any
import requests

from .base import BasePrinter

logger = logging.getLogger(__name__)


class YilianyunPrinter(BasePrinter):
    """易联云打印机实现"""
    
    API_BASE = "https://open-api.10ss.net"
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化易联云打印机
        
        Args:
            config: 必须包含 app_id, app_secret, machine_code
        """
        super().__init__(config)
        self.app_id = config["app_id"]
        self.app_secret = config["app_secret"]
        self.machine_code = config["machine_code"]
        
        logger.info(f"Initialized Yilianyun printer: {self.machine_code}")
    
    def _generate_sign(self, params: Dict[str, Any]) -> str:
        """
        生成易联云API签名
        
        签名算法：
        1. 将所有参数按key排序
        2. 拼接成 key1value1key2value2... 格式
        3. 末尾加上 app_secret
        4. MD5加密，转大写
        
        Args:
            params: API参数
            
        Returns:
            签名字符串
        """
        sorted_params = sorted(params.items())
        sign_str = ''.join([f"{k}{v}" for k, v in sorted_params]) + self.app_secret
        return hashlib.md5(sign_str.encode()).hexdigest().upper()
    
    def _call_api(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用易联云API
        
        Args:
            endpoint: API端点（如 /api/print）
            params: 业务参数
            
        Returns:
            API响应JSON
        """
        url = f"{self.API_BASE}{endpoint}"
        
        # 添加通用参数
        params["appid"] = self.app_id
        params["timestamp"] = str(int(time.time()))
        params["sign"] = self._generate_sign(params)
        
        try:
            logger.debug(f"Calling API {endpoint} with params: {params}")
            response = requests.post(url, data=params, timeout=self.timeout)
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"API response: {result}")
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"API timeout: {endpoint}")
            return {"error": "timeout", "error_description": "Request timeout"}
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {"error": "request_failed", "error_description": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": "unknown", "error_description": str(e)}
    
    def print_ticket(self, content: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        打印小票
        
        Args:
            content: 打印内容
            dry_run: 是否仅预览
            
        Returns:
            打印结果
        """
        if not self.validate_content(content):
            return {
                "success": False,
                "order_id": None,
                "message": "Invalid content",
                "preview": None
            }
        
        if dry_run or self.dry_run_mode:
            logger.info("Dry-run mode, no actual printing")
            return {
                "success": True,
                "order_id": None,
                "message": "Dry run mode",
                "preview": content[:200] + "..." if len(content) > 200 else content
            }
        
        # 生成唯一订单ID
        origin_id = f"order_{int(time.time() * 1000)}"
        
        params = {
            "machine_code": self.machine_code,
            "content": content,
            "origin_id": origin_id
        }
        
        result = self._call_api("/api/print", params)
        
        success = result.get("error") == "0"
        order_id = result.get("id")
        message = result.get("error_description", "Unknown error")
        
        if success:
            logger.info(f"Print success, order_id: {order_id}")
        else:
            logger.error(f"Print failed: {message}")
        
        return {
            "success": success,
            "order_id": order_id,
            "message": message,
            "preview": None
        }
    
    def query_status(self, order_id: str) -> Dict[str, Any]:
        """
        查询打印任务状态
        
        Args:
            order_id: 打印任务ID
            
        Returns:
            状态信息
        """
        params = {
            "machine_code": self.machine_code,
            "order_id": order_id
        }
        
        result = self._call_api("/api/queryOrderState", params)
        
        success = result.get("error") == "0"
        data = result.get("data", {})
        status = data.get("status", "unknown")
        
        # 状态映射
        status_map = {
            "0": "pending",
            "1": "printing", 
            "2": "completed",
            "3": "failed"
        }
        
        return {
            "success": success,
            "status": status_map.get(status, "unknown"),
            "printed": status == "2",
            "message": result.get("error_description", "")
        }
    
    def is_online(self) -> bool:
        """
        检查打印机是否在线
        
        Returns:
            是否在线
        """
        params = {"machine_code": self.machine_code}
        result = self._call_api("/api/queryPrinterStatus", params)
        
        if result.get("error") != "0":
            logger.warning(f"Failed to query printer status: {result}")
            return False
        
        data = result.get("data", {})
        status = data.get("status")
        
        is_online = status == "1"  # 1=在线, 0=离线
        logger.info(f"Printer online status: {is_online}")
        
        return is_online
