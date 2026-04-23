"""
订单翻译引擎
"""

import json
import os
import re
import logging
from typing import Optional, Dict, Any, Iterator

logger = logging.getLogger(__name__)


class OrderTranslator:
    """订单翻译引擎"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "qwen-turbo",
        base_url: Optional[str] = None
    ):
        """
        初始化翻译引擎
        
        Args:
            api_key: 大模型API Key，默认从环境变量QWEN_API_KEY读取
            model: 模型名称，默认通义千问turbo
            base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("QWEN_API_KEY")
        self.model = model
        self.base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        
        # 延迟导入openai，避免未安装时报错
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        except ImportError:
            logger.warning("openai package not installed, using mock mode")
            self.client = None
        
        # 加载prompts
        from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, build_few_shot_prompt
        self.system_prompt = SYSTEM_PROMPT
        self.user_prompt_template = USER_PROMPT_TEMPLATE
        self.build_few_shot = build_few_shot_prompt
    
    def translate(self, order_text: str, use_few_shot: bool = True) -> Dict[str, Any]:
        """
        将订单翻译为动作脚本
        
        Args:
            order_text: 原始订单文本，如"1x 拿铁（去冰，燕麦奶）"
            use_few_shot: 是否使用few-shot示例
            
        Returns:
            {
                "steps": list[str],
                "total_steps": int,
                "drink_name": str,
                "notes": str,
                "success": bool,
                "error": str (optional),
                "elapsed_time": float (optional)
            }
        """
        import time
        start_time = time.time()
        
        try:
            # 构建消息
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if use_few_shot:
                few_shot = self.build_few_shot()
                messages.append({"role": "user", "content": few_shot})
                messages.append({"role": "assistant", "content": "明白了，我会按照这些示例的格式输出。"})
            
            user_prompt = self.user_prompt_template.format(order_text=order_text)
            messages.append({"role": "user", "content": user_prompt})
            
            # 调用API
            if self.client is None:
                # Mock模式（测试用）
                result = self._mock_translate(order_text)
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.1,  # 低温度，更确定性
                    max_tokens=500
                )
                
                content = response.choices[0].message.content
                result = self._parse_response(content)
            
            # 验证结果
            if not self._validate_result(result):
                result["success"] = False
                result["error"] = "Validation failed"
            else:
                result["success"] = True
            
            elapsed = time.time() - start_time
            result["elapsed_time"] = round(elapsed, 2)
            
            logger.info(f"Translated '{order_text}' in {elapsed:.2f}s")
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Translation failed: {e}", exc_info=True)
            return {
                "steps": [],
                "total_steps": 0,
                "drink_name": "",
                "notes": "",
                "success": False,
                "error": str(e),
                "elapsed_time": round(elapsed, 2)
            }
    
    def _mock_translate(self, order_text: str) -> Dict[str, Any]:
        """
        Mock翻译（用于测试，无需真实API Key）
        
        Args:
            order_text: 订单文本
            
        Returns:
            模拟的翻译结果
        """
        # 简单的规则匹配
        order_lower = order_text.lower()
        
        # 识别饮品类型
        if "冰" in order_text or "iced" in order_lower:
            drink_type = "冰"
            cup_step = "拿冰杯"
        else:
            drink_type = "热"
            cup_step = "拿热杯"
        
        # 识别饮品名称
        if "拿铁" in order_text or "latte" in order_lower:
            drink_name = f"{drink_type}拿铁"
            steps = [cup_step, "加奶", "萃取倒入", "盖盖出杯"]
        elif "美式" in order_text or "americano" in order_lower:
            drink_name = f"{drink_type}美式"
            steps = [cup_step, "加水", "萃取倒入", "盖盖出杯"]
        elif "卡布奇诺" in order_text or "cappuccino" in order_lower:
            drink_name = f"{drink_type}卡布奇诺"
            steps = [cup_step, "加奶泡", "萃取倒入", "盖盖出杯"]
        elif "摩卡" in order_text or "mocha" in order_lower:
            drink_name = f"{drink_type}摩卡"
            steps = [cup_step, "加巧克力", "加奶", "萃取倒入", "盖盖出杯"]
        elif "焦糖" in order_text or "macchiato" in order_lower:
            drink_name = f"{drink_type}焦糖玛奇朵"
            steps = [cup_step, "加奶", "萃取倒入", "挤焦糖", "盖盖出杯"]
        else:
            drink_name = "未知饮品"
            steps = ["请杨老师协助"]
        
        # 识别规格
        notes = []
        if "大杯" in order_text:
            notes.append("大杯")
        if "燕麦奶" in order_text:
            notes.append("燕麦奶")
        if "脱脂" in order_text:
            notes.append("脱脂奶")
        if "半糖" in order_text:
            notes.append("半糖")
        if "无糖" in order_text:
            notes.append("无糖")
        if "少冰" in order_text:
            notes.append("少冰")
        if "去冰" in order_text:
            notes.append("去冰")
        if "加浓缩" in order_text:
            notes.append("加浓缩")
        
        return {
            "steps": steps,
            "total_steps": len(steps),
            "drink_name": drink_name,
            "notes": "、".join(notes) if notes else ""
        }
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """
        解析模型响应
        
        Args:
            content: 模型返回的文本
            
        Returns:
            解析后的字典
        """
        # 尝试直接解析
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        
        # 尝试从markdown代码块提取
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # 尝试找最大的{...}块
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        # 解析失败，返回原始内容
        logger.warning(f"Failed to parse response: {content[:100]}...")
        return {
            "steps": ["请杨老师协助"],
            "total_steps": 1,
            "drink_name": "解析失败",
            "notes": content[:50]
        }
    
    def _validate_result(self, result: Dict[str, Any]) -> bool:
        """
        验证翻译结果是否符合要求
        
        Args:
            result: 翻译结果
            
        Returns:
            是否有效
        """
        steps = result.get("steps", [])
        
        # 检查步骤存在且数量合理
        if not steps or len(steps) > 10:
            logger.warning(f"Invalid steps count: {len(steps) if steps else 0}")
            return False
        
        # 检查每步长度
        for step in steps:
            if len(step) > 20:
                logger.warning(f"Step too long: {step}")
                return False
        
        # 检查饮品名称
        if not result.get("drink_name"):
            logger.warning("Missing drink_name")
            return False
        
        return True


class BatchTranslator:
    """批量翻译器"""
    
    def __init__(self, translator: OrderTranslator):
        """
        初始化批量翻译器
        
        Args:
            translator: 翻译引擎实例
        """
        self.translator = translator
    
    def translate_orders(
        self,
        orders: list,
        continue_on_error: bool = True
    ) -> Iterator[Dict[str, Any]]:
        """
        批量翻译订单
        
        Args:
            orders: 订单文本列表
            continue_on_error: 出错时是否继续
            
        Yields:
            每个订单的翻译结果
        """
        for order in orders:
            try:
                result = self.translator.translate(order)
                yield {
                    "order": order,
                    "result": result,
                    "success": result.get("success", False)
                }
            except Exception as e:
                logger.error(f"Batch translation error for '{order}': {e}")
                if not continue_on_error:
                    raise
                yield {
                    "order": order,
                    "result": None,
                    "success": False,
                    "error": str(e)
                }
    
    def evaluate_accuracy(
        self,
        test_cases: list
    ) -> Dict[str, Any]:
        """
        评估翻译准确率
        
        Args:
            test_cases: 测试用例列表，每个包含input和expected
            
        Returns:
            评估结果
        """
        total = len(test_cases)
        passed = 0
        failures = []
        
        for case in test_cases:
            result = self.translator.translate(case["input"])
            
            # 简化的验证逻辑
            is_valid = self._check_result(result, case.get("expected"))
            
            if is_valid:
                passed += 1
            else:
                failures.append({
                    "input": case["input"],
                    "expected": case.get("expected"),
                    "actual": result
                })
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "accuracy": passed / total if total > 0 else 0,
            "failures": failures
        }
    
    def _check_result(self, result: Dict[str, Any], expected: Dict[str, Any]) -> bool:
        """
        检查结果是否符合预期
        
        Args:
            result: 实际结果
            expected: 预期结果
            
        Returns:
            是否通过
        """
        if not result.get("success"):
            return False
        
        # 检查关键字段
        if expected.get("drink_name"):
            if expected["drink_name"] not in result.get("drink_name", ""):
                return False
        
        if expected.get("min_steps"):
            if result.get("total_steps", 0) < expected["min_steps"]:
                return False
        
        return True
