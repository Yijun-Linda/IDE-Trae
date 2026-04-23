"""
飞鹅云打印机实现
API文档: https://www.feieyun.com/openapi.html
"""

import hashlib
import time
import logging
from typing import Dict, Any
import requests

from .base import BasePrinter

logger = logging.getLogger(__name__)


class FeiePrinter(BasePrinter):
    """飞鹅云打印机实现"""
    
    API_BASE = "https://api.feieyun.com"
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化飞鹅云打印机
        
        Args:
            config: 必须包含 user, ukey, sn
        """
        super().__init__(config)
        self.user = config["user"]
        self.ukey = config["ukey"]
        self.sn = config["sn"]
        
        logger.info(f"Initialized Feie printer: {self.sn}")
    
    def _generate_sign(self, stime: str) -> str:
        """
        生成飞鹅云API签名
        
        签名算法：sha1(user + ukey + stime)
        
        Args:
            stime: 时间戳字符串
            
        Returns:
            签名字符串
        """
        sign_str = self.user + self.ukey + stime
        return hashlib.sha1(sign_str.encode()).hexdigest()
    
    def _call_api(self, apiname: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用飞鹅云API
        
        Args:
            apiname: API名称（如 Open_printMsg）
            params: 业务参数
            
        Returns:
            API响应JSON
        """
        url = f"{self.API_BASE}/Api/Open/"
        
        stime = str(int(time.time()))
        
        # 构建请求参数
        request_params = {
            "user": self.user,
            "stime": stime,
            "sig": self._generate_sign(stime),
            "apiname": apiname
        }
        request_params.update(params)
        
        try:
            logger.debug(f"Calling API {apiname} with params: {params}")
            response = requests.post(url, data=request_params, timeout=self.timeout)
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"API response: {result}")
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"API timeout: {apiname}")
            return {"ret": -1, "msg": "Request timeout", "data": None}
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {"ret": -1, "msg": str(e), "data": None}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"ret": -1, "msg": str(e), "data": None}
    
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
        
        params = {
            "sn": self.sn,
            "content": content,
            "times": "1"  # 打印份数
        }
        
        result = self._call_api("Open_printMsg", params)
        
        ret = result.get("ret", -1)
        success = ret == 0
        order_id = result.get("data")
        message = result.get("msg", "Unknown error")
        
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
            "sn": self.sn,
            "orderid": order_id
        }
        
        result = self._call_api("Open_queryOrderState", params)
        
        ret = result.get("ret", -1)
        success = ret == 0
        data = result.get("data")
        
        # data: "0"=未打印, "1"=已打印
        is_printed = data == "1"
        
        return {
            "success": success,
            "status": "completed" if is_printed else "pending",
            "printed": is_printed,
            "message": result.get("msg", "")
        }
    
    def is_online(self) -> bool:
        """
        检查打印机是否在线
        
        Returns:
            是否在线
        """
        params = {"sn": self.sn}
        result = self._call_api("Open_queryPrinterStatus", params)
        
        ret = result.get("ret", -1)
        if ret != 0:
            logger.warning(f"Failed to query printer status: {result}")
            return False
        
        data = result.get("data", "")
        # 返回格式通常包含"在线"或"离线"
        is_online = "在线" in data
        
        logger.info(f"Printer online status: {is_online} ({data})")
        
        return is_online
