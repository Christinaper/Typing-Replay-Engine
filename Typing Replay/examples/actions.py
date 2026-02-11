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
    """
    text: str
    avg_char_delay: float = 0.1  # 平均每字符延迟（秒）
    delay_variance: float = 0.05  # 延迟抖动范围
    
    def execute(self, buffer: TextBuffer) -> None:
        """逐字符插入文本"""
        buffer.insert_text(self.text)
    
    def get_duration(self) -> float:
        """计算总持续时间"""
        total = 0.0
        for _ in self.text:
            # 为每个字符生成随机延迟
            delay = random.gauss(self.avg_char_delay, self.delay_variance)
            total += max(0.01, delay)  # 最小延迟 10ms
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
    """退格删除动作"""
    count: int = 1  # 删除字符数
    char_delay: float = 0.05  # 每次删除延迟
    
    def execute(self, buffer: TextBuffer) -> None:
        for _ in range(self.count):
            if not buffer.delete_char(forward=False):
                break
    
    def get_duration(self) -> float:
        return self.count * self.char_delay
    
    def __repr__(self) -> str:
        return f"BackspaceAction(count={self.count})"


@dataclass
class DeleteAction(Action):
    """Delete 键删除动作"""
    count: int = 1
    char_delay: float = 0.05
    
    def execute(self, buffer: TextBuffer) -> None:
        for _ in range(self.count):
            if not buffer.delete_char(forward=True):
                break
    
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
