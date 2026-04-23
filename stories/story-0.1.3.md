# Story-0.1.3: 极简小票模板设计与打印测试

## 关联信息
- 所属版本：v0.1
- 关联文档：mvp.md#2.1 核心交付物、visual_design.md#三、小票模板优化
- 前置依赖：story-0.1.1（打印机API）、story-0.1.2（翻译引擎）
- 优先级：P0

## 任务描述

设计并优化小票模板，确保打印效果清晰美观，心智障碍员工能够轻松阅读和理解。

### 设计要求
1. **极简原则**：删除所有装饰线、多余文字
2. **清晰可读**：字体大小适中，留白充足
3. **动作导向**：步骤前带勾选框，完成后可打勾
4. **认知友好**：一次只显示一杯的制作步骤

### 打印规格
- 纸张宽度：57mm（标准热敏纸）或 80mm
- 字体：打印机支持的宋体/黑体
- 字号：标题16pt加粗，正文14pt，备注12pt

## 认知约束

### 工作记忆是稀缺资源
- 小票上只显示当前这一杯的信息
- 不显示总订单数（避免干扰）
- 步骤不超过5步

### 被动接收优于主动检索
- 小票自动打印，员工无需主动获取
- 关键信息（杯号、步骤）一眼可见

### 不要搞特殊
- 小票外观与普通外卖小票相似
- 不增加员工的社会特殊感

## 完成标准

### 功能标准
- [ ] 小票模板设计完成（支持57mm和80mm两种宽度）
- [ ] 模板渲染引擎实现
- [ ] 勾选框支持（Unicode □/✓）
- [ ] 实际打印测试通过

### 验证标准
- [ ] 打印效果清晰可读（实地测试）
- [ ] 杨老师认可小票格式
- [ ] 模拟多订单场景，验证信息不混淆
- [ ] 代码覆盖率 > 80%

### 文档标准
- [ ] 小票设计规范文档（docs/dev0.1/0.1.3-ticket-template.md）
- [ ] 打印测试报告
- [ ] 模板使用说明

## 相关文件

- 代码路径：src/printer/
  - `template.py` - 模板渲染引擎
  - `formatter.py` - 文本格式化工具
- 模板文件：src/printer/templates/
  - `standard_57mm.txt` - 57mm标准模板
  - `standard_80mm.txt` - 80mm标准模板
- 测试路径：tests/test_template.py
- 文档路径：docs/dev0.1/0.1.3-ticket-template.md

## 技术细节

### 小票模板格式

```
┌────────────────────┐
│ 订单#128 第1/4杯    │  ← 16pt 加粗，居中
├────────────────────┤  ← 分隔线
│                    │
│ □ 1. 拿冰杯        │  ← 14pt，勾选框+序号
│                    │
│ □ 2. 加冰块、燕麦奶 │  ← 14pt
│                    │
│ □ 3. 萃取、倒入、盖盖│  ← 14pt
│                    │
├────────────────────┤
│ 5分钟后出下一杯     │  ← 12pt 灰色，居中
└────────────────────┘
```

### 模板渲染引擎

```python
class TicketTemplate:
    """小票模板渲染器"""
    
    def __init__(self, width_mm: int = 57):
        self.width_mm = width_mm
        self.chars_per_line = 16 if width_mm == 57 else 24
    
    def render(self, order_id: str, current: int, total: int, 
               drink_name: str, steps: list[str], 
               delay_minutes: int = 5) -> str:
        """
        渲染小票内容
        
        Args:
            order_id: 订单号
            current: 当前杯数
            total: 总杯数
            drink_name: 饮品名称
            steps: 制作步骤列表
            delay_minutes: 下一杯延迟时间
            
        Returns:
            格式化后的小票文本（ESC/POS指令或纯文本）
        """
        pass
    
    def _center(self, text: str) -> str:
        """文本居中"""
        pass
    
    def _bold(self, text: str) -> str:
        """加粗文本"""
        pass
```

### ESC/POS指令支持

云打印机通常支持ESC/POS指令控制格式：

```python
# ESC/POS 指令常量
ESC = '\x1b'
GS = '\x1d'
ALIGN_CENTER = ESC + 'a' + '\x01'
ALIGN_LEFT = ESC + 'a' + '\x00'
BOLD_ON = ESC + 'E' + '\x01'
BOLD_OFF = ESC + 'E' + '\x00'
CUT_PAPER = GS + 'V' + '\x01'
```

### 纯文本回退模式

当ESC/POS指令不被支持时，使用纯文本+空格对齐：

```python
def render_plain_text(self, ...) -> str:
    """纯文本模式渲染（兼容性更好）"""
    lines = []
    # 标题居中
    title = f"订单#{order_id} 第{current}/{total}杯"
    lines.append(title.center(self.chars_per_line))
    lines.append("=" * self.chars_per_line)
    
    # 步骤
    for i, step in enumerate(steps, 1):
        lines.append(f"□ {i}. {step}")
        lines.append("")  # 空行
    
    # 底部提示
    lines.append("-" * self.chars_per_line)
    lines.append(f"{delay_minutes}分钟后出下一杯".center(self.chars_per_line))
    
    return "\n".join(lines)
```

## 状态
- [x] 待开始 / [ ] 进行中 / [ ] 已完成

## 备注

### 打印测试清单

| 测试项 | 通过标准 |
|--------|---------|
| 字体清晰度 | 1米外可清晰阅读 |
| 勾选框可见性 | □符号不模糊 |
| 留白充足 | 行间距适中，不拥挤 |
| 裁切位置 | 内容完整，不裁切文字 |
| 多订单连续打印 | 每张之间有明显分隔 |

### 风险与应对
| 风险 | 应对措施 |
|------|---------|
| 57mm纸张太窄 | 同时提供80mm模板，根据实际设备选择 |
| 热敏纸褪色快 | 使用高质量热敏纸，提醒员工及时完成 |
| 打印机不支持ESC/POS | 提供纯文本回退模式 |
| 中文显示乱码 | 使用GBK编码，测试常见打印机 |
