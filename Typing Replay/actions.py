"""
行为/动作抽象 (Action)
定义所有可执行的编辑操作
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Callable
import random
import time

from buffer import TextBuffer, TextStyle


# Emoji 快捷码映射表
EMOJI_SHORTCUTS = {
    ':smile:': '😊',
    ':grin:': '😀',
    ':laugh:': '😄',
    ':happy:': '😃',
    ':wink:': '😉',
    ':heart:': '❤️',
    ':like:': '👍',
    ':fire:': '🔥',
    ':star:': '⭐',
    ':check:': '✅',
    ':cross:': '❌',
    ':rocket:': '🚀',
    ':party:': '🎉',
    ':sparkles:': '✨',
    ':tada:': '🎊',
    ':cry:': '😢',
    ':sad:': '😞',
    ':angry:': '😠',
    ':cool:': '😎',
    ':think:': '🤔',
    ':muscle:': '💪',
    ':pray:': '🙏',
    ':clap:': '👏',
    ':wave:': '👋',
    ':eye:': '👀',
    ':100:': '💯',
    ':ok:': '👌',
    ':point:': '👉',
    ':hand:': '✋',
    ':coffee:': '☕',
    ':pizza:': '🍕',
    ':beer:': '🍺',
    ':cake:': '🎂',
    ':gift:': '🎁',
    ':book:': '📖',
    ':pen:': '✏️',
    ':mail:': '📧',
    ':phone:': '📱',
    ':computer:': '💻',
    ':bulb:': '💡',
    ':lock:': '🔒',
    ':key:': '🔑',
    ':warning:': '⚠️',
    ':info:': 'ℹ️',
    ':question:': '❓',
    ':exclamation:': '❗',
    ':sun:': '☀️',
    ':moon:': '🌙',
    ':cloud:': '☁️',
    ':rain:': '🌧️',
    ':snow:': '❄️',
    ':tree:': '🌲',
    ':flower:': '🌸',
    ':rose:': '🌹',
    ':cat:': '🐱',
    ':dog:': '🐶',
    ':bird:': '🐦',
    ':fish:': '🐟',
}


def expand_emoji_shortcuts(text: str) -> str:
    """
    展开文本中的 emoji 快捷码
    
    Args:
        text: 包含快捷码的文本，如 "Hello :smile:"
    
    Returns:
        展开后的文本，如 "Hello 😊"
    """
    result = text
    for shortcut, emoji in EMOJI_SHORTCUTS.items():
        result = result.replace(shortcut, emoji)
    return result


class Action(ABC):
    """动作基类"""
    
    @abstractmethod
    def execute(self, buffer: TextBuffer) -> None:
        """
        执行动作
        
        Args:
            buffer: 文本缓冲区
        """
        pass
    
    @abstractmethod
    def get_duration(self) -> float:
        """
        获取动作持续时间（秒）
        
        Returns:
            持续时间
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


# ==================== 基础文本操作 ====================

@dataclass
class TypeTextAction(Action):
    """
    逐字符打字动作
    支持速度控制和随机抖动
    支持 emoji 快捷码（如 :smile: → 😊）
    注意：这个动作在执行时会被分解为多个单字符插入
    """
    text: str
    avg_char_delay: float = 0.1  # 平均每字符延迟（秒）
    delay_variance: float = 0.05  # 延迟抖动范围
    expand_emoji: bool = True  # 是否展开 emoji 快捷码
    
    def __post_init__(self):
        """初始化后处理 - 展开 emoji"""
        if self.expand_emoji:
            self.text = expand_emoji_shortcuts(self.text)
    
    def execute(self, buffer: TextBuffer) -> None:
        """一次性插入所有文本（用于非实时播放）"""
        buffer.insert_text(self.text)
    
    def execute_char_by_char(self, buffer: TextBuffer, char_index: int) -> bool:
        """
        逐字符执行（用于实时播放）
        
        Args:
            buffer: 文本缓冲区
            char_index: 当前字符索引
        
        Returns:
            是否还有更多字符
        """
        if char_index < len(self.text):
            buffer.insert_text(self.text[char_index])
            return char_index + 1 < len(self.text)
        return False
    
    def get_char_delay(self, char_index: int) -> float:
        """获取指定字符的延迟"""
        delay = random.gauss(self.avg_char_delay, self.delay_variance)
        return max(0.01, delay)  # 最小延迟 10ms
    
    def get_duration(self) -> float:
        """计算总持续时间"""
        total = 0.0
        for i in range(len(self.text)):
            total += self.get_char_delay(i)
        return total
    
    def __repr__(self) -> str:
        preview = self.text[:20] + "..." if len(self.text) > 20 else self.text
        return f"TypeTextAction('{preview}', {len(self.text)} chars)"


@dataclass
class InsertTextAction(Action):
    """
    即时插入文本动作（无打字延迟）
    用于粘贴等操作
    """
    text: str
    duration: float = 0.05  # 固定持续时间
    
    def execute(self, buffer: TextBuffer) -> None:
        buffer.insert_text(self.text)
    
    def get_duration(self) -> float:
        return self.duration
    
    def __repr__(self) -> str:
        preview = self.text[:20] + "..." if len(self.text) > 20 else self.text
        return f"InsertTextAction('{preview}')"


@dataclass
class BackspaceAction(Action):
    """退格删除动作 - 逐字符删除"""
    count: int = 1  # 删除字符数
    char_delay: float = 0.05  # 每次删除延迟
    
    def execute(self, buffer: TextBuffer) -> None:
        """一次性删除所有字符（用于非实时播放）"""
        for _ in range(self.count):
            if not buffer.delete_char(forward=False):
                break
    
    def execute_step_by_step(self, buffer: TextBuffer, step_index: int) -> bool:
        """
        逐步删除（用于实时播放）
        
        Args:
            buffer: 文本缓冲区
            step_index: 当前步骤索引
        
        Returns:
            是否还有更多步骤
        """
        if step_index < self.count:
            buffer.delete_char(forward=False)
            return step_index + 1 < self.count
        return False
    
    def get_duration(self) -> float:
        return self.count * self.char_delay
    
    def __repr__(self) -> str:
        return f"BackspaceAction(count={self.count})"


@dataclass
class DeleteAction(Action):
    """Delete 键删除动作 - 逐字符删除"""
    count: int = 1
    char_delay: float = 0.05
    
    def execute(self, buffer: TextBuffer) -> None:
        """一次性删除所有字符（用于非实时播放）"""
        for _ in range(self.count):
            if not buffer.delete_char(forward=True):
                break
    
    def execute_step_by_step(self, buffer: TextBuffer, step_index: int) -> bool:
        """
        逐步删除（用于实时播放）
        
        Args:
            buffer: 文本缓冲区
            step_index: 当前步骤索引
        
        Returns:
            是否还有更多步骤
        """
        if step_index < self.count:
            buffer.delete_char(forward=True)
            return step_index + 1 < self.count
        return False
    
    def get_duration(self) -> float:
        return self.count * self.char_delay
    
    def __repr__(self) -> str:
        return f"DeleteAction(count={self.count})"


@dataclass
class ReplaceTextAction(Action):
    """替换文本动作"""
    start: int
    end: int
    new_text: str
    duration: float = 0.1
    
    def execute(self, buffer: TextBuffer) -> None:
        buffer.replace_text(self.start, self.end, self.new_text)
    
    def get_duration(self) -> float:
        return self.duration
    
    def __repr__(self) -> str:
        return f"ReplaceTextAction([{self.start}:{self.end}] -> '{self.new_text[:20]}')"


# ==================== 光标与选区操作 ====================

@dataclass
class MoveCursorAction(Action):
    """移动光标动作"""
    position: Optional[int] = None  # 绝对位置
    offset: Optional[int] = None  # 相对偏移
    clear_selection: bool = True
    duration: float = 0.02
    
    def execute(self, buffer: TextBuffer) -> None:
        if self.position is not None:
            buffer.move_cursor(self.position, self.clear_selection)
        elif self.offset is not None:
            buffer.move_cursor_relative(self.offset, self.clear_selection)
        else:
            raise ValueError("Must specify either position or offset")
    
    def get_duration(self) -> float:
        return self.duration
    
    def __repr__(self) -> str:
        if self.position is not None:
            return f"MoveCursorAction(pos={self.position})"
        return f"MoveCursorAction(offset={self.offset})"


@dataclass
class SetSelectionAction(Action):
    """设置选区动作"""
    start: int
    end: int
    duration: float = 0.05
    
    def execute(self, buffer: TextBuffer) -> None:
        buffer.set_selection(self.start, self.end)
    
    def get_duration(self) -> float:
        return self.duration
    
    def __repr__(self) -> str:
        return f"SetSelectionAction([{self.start}:{self.end}])"


@dataclass
class SelectRangeAction(Action):
    """从当前位置选择指定长度"""
    start: int
    length: int
    duration: float = 0.05
    
    def execute(self, buffer: TextBuffer) -> None:
        buffer.select_range(self.start, self.length)
    
    def get_duration(self) -> float:
        return self.duration
    
    def __repr__(self) -> str:
        return f"SelectRangeAction(start={self.start}, len={self.length})"


@dataclass
class ClearSelectionAction(Action):
    """清除选区动作"""
    duration: float = 0.01
    
    def execute(self, buffer: TextBuffer) -> None:
        buffer.clear_selection()
    
    def get_duration(self) -> float:
        return self.duration


@dataclass
class DeleteSelectionAction(Action):
    """删除选区内容动作"""
    duration: float = 0.05
    
    def execute(self, buffer: TextBuffer) -> None:
        buffer.delete_selection()
    
    def get_duration(self) -> float:
        return self.duration


# ==================== 样式操作 ====================

@dataclass
class SetStyleAction(Action):
    """设置文本样式动作"""
    style: TextStyle
    duration: float = 0.01
    
    def execute(self, buffer: TextBuffer) -> None:
        buffer.set_style(self.style)
    
    def get_duration(self) -> float:
        return self.duration
    
    def __repr__(self) -> str:
        return f"SetStyleAction({self.style.value})"


# ==================== 控制操作 ====================

@dataclass
class PauseAction(Action):
    """停顿动作"""
    duration: float
    
    def execute(self, buffer: TextBuffer) -> None:
        # 停顿不改变缓冲区状态
        pass
    
    def get_duration(self) -> float:
        return self.duration
    
    def __repr__(self) -> str:
        return f"PauseAction({self.duration}s)"


@dataclass
class CallbackAction(Action):
    """
    回调动作
    允许执行自定义函数
    """
    callback: Callable[[TextBuffer], None]
    name: str = "callback"
    duration: float = 0.0
    
    def execute(self, buffer: TextBuffer) -> None:
        self.callback(buffer)
    
    def get_duration(self) -> float:
        return self.duration
    
    def __repr__(self) -> str:
        return f"CallbackAction({self.name})"


# ==================== 组合操作 ====================

@dataclass
class CompositeAction(Action):
    """
    组合动作
    按顺序执行多个子动作
    """
    actions: list[Action]
    
    def execute(self, buffer: TextBuffer) -> None:
        for action in self.actions:
            action.execute(buffer)
    
    def get_duration(self) -> float:
        return sum(action.get_duration() for action in self.actions)
    
    def __repr__(self) -> str:
        return f"CompositeAction({len(self.actions)} actions)"


# ==================== 便捷工厂函数 ====================

def type_text(text: str, wpm: int = 60, variance: float = 0.3) -> TypeTextAction:
    """
    创建打字动作的便捷函数
    
    Args:
        text: 要打字的文本
        wpm: 每分钟单词数 (假设平均 5 字符/单词)
        variance: 延迟方差系数 (0.0-1.0)
    
    Returns:
        TypeTextAction
    """
    # 计算每字符平均延迟
    chars_per_second = (wpm * 5) / 60
    avg_delay = 1.0 / chars_per_second
    delay_variance = avg_delay * variance
    
    return TypeTextAction(text, avg_delay, delay_variance)


def pause(seconds: float) -> PauseAction:
    """创建停顿动作"""
    return PauseAction(seconds)


def backspace(count: int = 1) -> BackspaceAction:
    """创建退格动作"""
    return BackspaceAction(count)


def move_cursor(position: int) -> MoveCursorAction:
    """移动光标到绝对位置"""
    return MoveCursorAction(position=position)


def move_cursor_by(offset: int) -> MoveCursorAction:
    """相对移动光标"""
    return MoveCursorAction(offset=offset)


def select(start: int, end: int) -> SetSelectionAction:
    """创建选区"""
    return SetSelectionAction(start, end)


def delete_selection() -> DeleteSelectionAction:
    """删除选区"""
    return DeleteSelectionAction()


def set_style(style: TextStyle) -> SetStyleAction:
    """设置样式"""
    return SetStyleAction(style)
