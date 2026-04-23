"""
小票模板渲染器
"""

from dataclasses import dataclass
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class TicketData:
    """小票数据模型"""
    order_id: str                    # 订单号
    current: int                     # 当前杯数
    total: int                       # 总杯数
    drink_name: str                  # 饮品名称
    steps: List[str]                 # 制作步骤
    notes: Optional[str] = None      # 备注（规格信息）
    delay_minutes: int = 5           # 下一杯延迟时间


@dataclass
class TicketConfig:
    """小票配置"""
    width_mm: int = 57               # 纸张宽度
    title_font_size: int = 16        # 标题字号
    body_font_size: int = 14         # 正文字号
    small_font_size: int = 12        # 小字号
    line_spacing: int = 1            # 行间距倍数
    chars_per_line: int = 16         # 每行字符数


class TicketTemplate:
    """小票模板渲染器"""
    
    # ESC/POS 指令常量
    ESC = '\x1b'
    GS = '\x1d'
    ALIGN_CENTER = ESC + 'a' + '\x01'
    ALIGN_LEFT = ESC + 'a' + '\x00'
    BOLD_ON = ESC + 'E' + '\x01'
    BOLD_OFF = ESC + 'E' + '\x00'
    LINE_FEED = '\n'
    CUT_PAPER = GS + 'V' + '\x01'
    
    def __init__(self, config: Optional[TicketConfig] = None):
        """
        初始化模板
        
        Args:
            config: 模板配置，默认57mm标准配置
        """
        self.config = config or TicketConfig()
        self.use_esc_pos = True  # 是否使用ESC/POS指令
    
    def render(self, data: TicketData) -> str:
        """
        渲染小票
        
        Args:
            data: 小票数据
            
        Returns:
            格式化后的小票内容（ESC/POS指令或纯文本）
        """
        if self.use_esc_pos:
            return self._render_esc_pos(data)
        else:
            return self._render_plain_text(data)
    
    def _render_esc_pos(self, data: TicketData) -> str:
        """
        使用ESC/POS指令渲染
        
        Args:
            data: 小票数据
            
        Returns:
            ESC/POS指令字符串
        """
        lines = []
        
        # 初始化打印机
        lines.append(self.ESC + '@')
        
        # 标题（加粗、居中）
        lines.append(self.ALIGN_CENTER)
        lines.append(self.BOLD_ON)
        lines.append(f"订单#{data.order_id} 第{data.current}/{data.total}杯")
        lines.append(self.BOLD_OFF)
        lines.append(self.LINE_FEED)
        
        # 饮品名（加粗、居中）
        lines.append(self.BOLD_ON)
        lines.append(data.drink_name)
        lines.append(self.BOLD_OFF)
        lines.append(self.LINE_FEED)
        
        # 分隔线
        lines.append(self.ALIGN_LEFT)
        lines.append("=" * self.config.chars_per_line)
        lines.append(self.LINE_FEED)
        
        # 步骤
        for i, step in enumerate(data.steps, 1):
            lines.append(f"□ {i}. {step}")
            lines.append(self.LINE_FEED)
            lines.append(self.LINE_FEED)  # 空行
        
        # 分隔线
        lines.append("-" * self.config.chars_per_line)
        lines.append(self.LINE_FEED)
        
        # 底部提示（居中）
        lines.append(self.ALIGN_CENTER)
        lines.append(f"{data.delay_minutes}分钟后出下一杯")
        lines.append(self.LINE_FEED)
        
        # 切纸
        lines.append(self.CUT_PAPER)
        
        return "".join(lines)
    
    def _render_plain_text(self, data: TicketData) -> str:
        """
        纯文本渲染（兼容性更好）
        
        Args:
            data: 小票数据
            
        Returns:
            纯文本字符串
        """
        lines = []
        width = self.config.chars_per_line
        
        # 标题居中
        title = f"订单#{data.order_id} 第{data.current}/{data.total}杯"
        lines.append(title.center(width))
        lines.append("")
        
        # 饮品名居中
        lines.append(data.drink_name.center(width))
        lines.append("")
        
        # 分隔线
        lines.append("=" * width)
        lines.append("")
        
        # 步骤
        for i, step in enumerate(data.steps, 1):
            lines.append(f"□ {i}. {step}")
            lines.append("")  # 空行
        
        # 分隔线
        lines.append("-" * width)
        lines.append("")
        
        # 底部提示
        footer = f"{data.delay_minutes}分钟后出下一杯"
        lines.append(footer.center(width))
        
        return "\n".join(lines)


class TemplateFactory:
    """模板工厂"""
    
    @staticmethod
    def create_57mm_template() -> TicketTemplate:
        """
        创建57mm标准模板
        
        Returns:
            57mm模板实例
        """
        config = TicketConfig(
            width_mm=57,
            chars_per_line=16,
            title_font_size=16,
            body_font_size=14,
            small_font_size=12
        )
        return TicketTemplate(config)
    
    @staticmethod
    def create_80mm_template() -> TicketTemplate:
        """
        创建80mm标准模板
        
        Returns:
            80mm模板实例
        """
        config = TicketConfig(
            width_mm=80,
            chars_per_line=24,
            title_font_size=16,
            body_font_size=14,
            small_font_size=12
        )
        return TicketTemplate(config)
    
    @staticmethod
    def create_simple_template() -> TicketTemplate:
        """
        创建纯文本简化模板（最大兼容性）
        
        Returns:
            纯文本模板实例
        """
        template = TicketTemplate()
        template.use_esc_pos = False
        return template
