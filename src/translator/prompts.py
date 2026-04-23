"""
Prompt模板定义
"""

import json

# 系统Prompt
SYSTEM_PROMPT = """你是一个咖啡制作指导助手，专门为心智障碍员工设计。

你的任务是将顾客的订单翻译为简单、清晰的咖啡制作步骤。

## 输出格式要求
必须输出JSON格式：
{
  "steps": ["步骤1", "步骤2", ...],
  "total_steps": 步骤数量,
  "drink_name": "饮品名称",
  "notes": "备注信息（规格、特殊要求）"
}

## 步骤设计原则
1. 每步不超过10个汉字
2. 使用动作动词：拿、加、倒、盖、按、放
3. 避免抽象词：适量、少许、一些
4. 按时间顺序排列
5. 总步骤控制在3-6步

## 规格映射规则
- 杯型：中杯（默认）、大杯（加量）
- 牛奶：全脂（默认）、燕麦奶、脱脂奶
- 甜度：无糖、半糖、全糖（默认）
- 冰量：正常冰、少冰、去冰
- 加料：加浓缩（额外一步）

## 支持的饮品
热饮：美式咖啡、拿铁、卡布奇诺、摩卡、焦糖玛奇朵
冷饮：冰美式、冰拿铁、冰卡布奇诺、冰摩卡、冰焦糖玛奇朵

## 示例

输入：1x 拿铁（大杯，燕麦奶）
输出：
{
  "steps": ["拿热杯大杯", "加燕麦奶", "萃取浓缩", "倒入混合", "盖盖出杯"],
  "total_steps": 5,
  "drink_name": "热拿铁",
  "notes": "大杯"
}

输入：1x 冰美式（少冰）
输出：
{
  "steps": ["拿冰杯中杯", "加少量冰", "加水八分满", "萃取倒入", "盖盖出杯"],
  "total_steps": 5,
  "drink_name": "冰美式",
  "notes": "少冰"
}"""

# 用户Prompt模板
USER_PROMPT_TEMPLATE = """请将以下订单翻译为制作步骤：

订单内容：{order_text}

要求：
1. 识别饮品名称和规格
2. 按步骤设计原则拆解
3. 输出JSON格式
4. 确保步骤可被心智障碍员工理解

请直接输出JSON，不要包含其他说明文字。"""

# Few-shot示例
FEW_SHOT_EXAMPLES = [
    {
        "input": "1x 美式咖啡",
        "output": {
            "steps": ["拿热杯中杯", "萃取浓缩", "加水八分满", "盖盖出杯"],
            "total_steps": 4,
            "drink_name": "热美式",
            "notes": ""
        }
    },
    {
        "input": "1x 拿铁（大杯，燕麦奶，半糖）",
        "output": {
            "steps": ["拿热杯大杯", "加燕麦奶", "加半糖糖浆", "萃取倒入", "盖盖出杯"],
            "total_steps": 5,
            "drink_name": "热拿铁",
            "notes": "大杯、半糖"
        }
    },
    {
        "input": "1x 冰拿铁（去冰，脱脂奶）",
        "output": {
            "steps": ["拿冰杯", "不加冰", "加脱脂奶", "萃取倒入", "盖盖出杯"],
            "total_steps": 5,
            "drink_name": "冰拿铁",
            "notes": "去冰、脱脂奶"
        }
    },
    {
        "input": "1x 摩卡（加浓缩）",
        "output": {
            "steps": ["拿热杯", "加巧克力酱", "加奶", "萃取双份", "倒入混合", "盖盖出杯"],
            "total_steps": 6,
            "drink_name": "热摩卡",
            "notes": "加浓缩"
        }
    },
    {
        "input": "1x 焦糖玛奇朵（大杯）",
        "output": {
            "steps": ["拿热杯大杯", "加奶", "萃取浓缩", "挤焦糖酱", "盖盖出杯"],
            "total_steps": 5,
            "drink_name": "热焦糖玛奇朵",
            "notes": "大杯"
        }
    }
]


def build_few_shot_prompt(examples: list = None) -> str:
    """
    构建few-shot提示
    
    Args:
        examples: 示例列表，默认使用FEW_SHOT_EXAMPLES
        
    Returns:
        few-shot提示文本
    """
    if examples is None:
        examples = FEW_SHOT_EXAMPLES
    
    lines = ["## 参考示例\n"]
    for i, ex in enumerate(examples, 1):
        lines.append(f"示例{i}：")
        lines.append(f"输入：{ex['input']}")
        lines.append(f"输出：{json.dumps(ex['output'], ensure_ascii=False)}")
        lines.append("")
    
    return "\n".join(lines)
