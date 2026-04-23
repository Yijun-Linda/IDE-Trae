"""
打印机模块单元测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

# 导入被测模块
import sys
sys.path.insert(0, 'd:\\tuzizhang99\\vibe-muse\\IDE-Trae\\src')

from printer.yilianyun import YilianyunPrinter
from printer.feie import FeiePrinter
from printer.factory import PrinterFactory


class TestYilianyunPrinter:
    """易联云打印机测试"""
    
    @pytest.fixture
    def config(self):
        return {
            "app_id": "test_app_id",
            "app_secret": "test_secret",
            "machine_code": "test_machine",
            "timeout": 5
        }
    
    @pytest.fixture
    def printer(self, config):
        return YilianyunPrinter(config)
    
    def test_init(self, printer, config):
        """测试初始化"""
        assert printer.app_id == config["app_id"]
        assert printer.app_secret == config["app_secret"]
        assert printer.machine_code == config["machine_code"]
        assert printer.timeout == config["timeout"]
    
    def test_validate_content_empty(self, printer):
        """测试空内容验证"""
        assert printer.validate_content("") == False
        assert printer.validate_content(None) == False
    
    def test_validate_content_too_long(self, printer):
        """测试超长内容验证"""
        assert printer.validate_content("x" * 5000) == False
    
    def test_validate_content_valid(self, printer):
        """测试有效内容验证"""
        assert printer.validate_content("有效内容") == True
        assert printer.validate_content("x" * 1000) == True
    
    def test_generate_sign(self, printer):
        """测试签名生成"""
        params = {"key1": "value1", "key2": "value2"}
        sign = printer._generate_sign(params)
        
        # 签名应该是32位大写MD5
        assert len(sign) == 32
        assert sign.isupper()
    
    def test_print_ticket_dry_run(self, printer):
        """测试dry-run模式"""
        result = printer.print_ticket("测试内容", dry_run=True)
        
        assert result["success"] == True
        assert result["preview"] is not None
        assert result["order_id"] is None
        assert "Dry run" in result["message"]
    
    @patch('printer.yilianyun.requests.post')
    def test_print_ticket_success(self, mock_post, printer):
        """测试打印成功"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": "0",
            "id": "12345",
            "error_description": "Success"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = printer.print_ticket("测试内容")
        
        assert result["success"] == True
        assert result["order_id"] == "12345"
        assert result["message"] == "Success"
    
    @patch('printer.yilianyun.requests.post')
    def test_print_ticket_failure(self, mock_post, printer):
        """测试打印失败"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": "1",
            "error_description": "Printer offline"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = printer.print_ticket("测试内容")
        
        assert result["success"] == False
        assert result["message"] == "Printer offline"
    
    @patch('printer.yilianyun.requests.post')
    def test_query_status(self, mock_post, printer):
        """测试查询状态"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": "0",
            "data": {"status": "2"}  # 2=已完成
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = printer.query_status("order_123")
        
        assert result["success"] == True
        assert result["status"] == "completed"
        assert result["printed"] == True
    
    @patch('printer.yilianyun.requests.post')
    def test_is_online(self, mock_post, printer):
        """测试在线状态检查"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": "0",
            "data": {"status": "1"}  # 1=在线
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        assert printer.is_online() == True


class TestFeiePrinter:
    """飞鹅云打印机测试"""
    
    @pytest.fixture
    def config(self):
        return {
            "user": "test_user",
            "ukey": "test_ukey",
            "sn": "test_sn",
            "timeout": 5
        }
    
    @pytest.fixture
    def printer(self, config):
        return FeiePrinter(config)
    
    def test_init(self, printer, config):
        """测试初始化"""
        assert printer.user == config["user"]
        assert printer.ukey == config["ukey"]
        assert printer.sn == config["sn"]
    
    def test_generate_sign(self, printer):
        """测试签名生成"""
        stime = "1234567890"
        sign = printer._generate_sign(stime)
        
        # 签名应该是40位SHA1
        assert len(sign) == 40
    
    @patch('printer.feie.requests.post')
    def test_print_ticket_success(self, mock_post, printer):
        """测试打印成功"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "ret": 0,
            "data": "ORDER123",
            "msg": "Success"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = printer.print_ticket("测试内容")
        
        assert result["success"] == True
        assert result["order_id"] == "ORDER123"
    
    @patch('printer.feie.requests.post')
    def test_is_online(self, mock_post, printer):
        """测试在线状态检查"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "ret": 0,
            "data": "在线"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        assert printer.is_online() == True


class TestPrinterFactory:
    """打印机工厂测试"""
    
    def test_create_yilianyun(self):
        """测试创建易联云打印机"""
        config = {
            "app_id": "test",
            "app_secret": "test",
            "machine_code": "test"
        }
        
        printer = PrinterFactory.create("yilianyun", config)
        
        assert isinstance(printer, YilianyunPrinter)
    
    def test_create_feie(self):
        """测试创建飞鹅打印机"""
        config = {
            "user": "test",
            "ukey": "test",
            "sn": "test"
        }
        
        printer = PrinterFactory.create("feie", config)
        
        assert isinstance(printer, FeiePrinter)
    
    def test_create_unknown_provider(self):
        """测试未知厂商"""
        with pytest.raises(ValueError) as exc_info:
            PrinterFactory.create("unknown", {})
        
        assert "Unknown printer provider" in str(exc_info.value)
    
    def test_list_providers(self):
        """测试列出厂商"""
        providers = PrinterFactory.list_providers()
        
        assert "yilianyun" in providers
        assert "feie" in providers


class TestBasePrinter:
    """打印机基类测试"""
    
    def test_dry_run_mode(self):
        """测试dry-run模式设置"""
        from printer.base import BasePrinter
        
        # 创建具体实现用于测试
        class TestPrinter(BasePrinter):
            def print_ticket(self, content, dry_run=False):
                return {"success": True}
            
            def query_status(self, order_id):
                return {"success": True}
            
            def is_online(self):
                return True
        
        printer = TestPrinter({"timeout": 10})
        
        assert printer.dry_run_mode == False
        
        printer.set_dry_run(True)
        assert printer.dry_run_mode == True
        
        printer.set_dry_run(False)
        assert printer.dry_run_mode == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
