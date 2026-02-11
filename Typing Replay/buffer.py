"""
编辑状态模型 (Buffer / Cursor / Selection)
管理文本缓冲区、光标位置和选区状态
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple
from enum import Enum


class TextStyle(Enum):
    """文本样式枚举"""
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    CODE = "code"


@dataclass
class Selection:
    """选区状态"""
    start: int
    end: int
    
    def __post_init__(self):
        """确保 start <= end"""
        if self.start > self.end:
            self.start, self.end = self.end, self.start
    
    @property
    def length(self) -> int:
        """选区长度"""
        return self.end - self.start
    
    @property
    def is_empty(self) -> bool:
        """是否为空选区"""
        return self.start == self.end
    
    def __repr__(self) -> str:
        return f"Selection({self.start}, {self.end})"


@dataclass
class EditorState:
    """编辑器完整状态快照"""
    text: str
    cursor_pos: int
    selection: Optional[Selection]
    current_style: TextStyle
    timestamp: float
    
    def __repr__(self) -> str:
        sel_repr = f", selection={self.selection}" if self.selection else ""
        return (f"EditorState(text_len={len(self.text)}, "
                f"cursor={self.cursor_pos}{sel_repr}, "
                f"style={self.current_style.value})")


class TextBuffer:
    """
    文本缓冲区管理器
    维护文本内容、光标位置、选区和样式状态
    """
    
    def __init__(self):
        self._text: str = ""
        self._cursor: int = 0
        self._selection: Optional[Selection] = None
        self._current_style: TextStyle = TextStyle.NORMAL
        self._style_ranges: list[Tuple[int, int, TextStyle]] = []
    
    # ==================== 基础属性 ====================
    
    @property
    def text(self) -> str:
        """获取当前文本"""
        return self._text
    
    @property
    def cursor(self) -> int:
        """获取光标位置"""
        return self._cursor
    
    @property
    def selection(self) -> Optional[Selection]:
        """获取当前选区"""
        return self._selection
    
    @property
    def current_style(self) -> TextStyle:
        """获取当前样式"""
        return self._current_style
    
    @property
    def length(self) -> int:
        """获取文本长度"""
        return len(self._text)
    
    # ==================== 光标操作 ====================
    
    def move_cursor(self, position: int, clear_selection: bool = True) -> None:
        """
        移动光标到指定位置
        
        Args:
            position: 目标位置 (0 到 len(text))
            clear_selection: 是否清除选区
        """
        position = max(0, min(position, self.length))
        self._cursor = position
        
        if clear_selection:
            self._selection = None
    
    def move_cursor_relative(self, offset: int, clear_selection: bool = True) -> None:
        """
        相对移动光标
        
        Args:
            offset: 偏移量 (正数向右，负数向左)
            clear_selection: 是否清除选区
        """
        self.move_cursor(self._cursor + offset, clear_selection)
    
    # ==================== 选区操作 ====================
    
    def set_selection(self, start: int, end: int) -> None:
        """
        设置选区
        
        Args:
            start: 起始位置
            end: 结束位置
        """
        start = max(0, min(start, self.length))
        end = max(0, min(end, self.length))
        
        self._selection = Selection(start, end)
        self._cursor = end  # 光标通常在选区末尾
    
    def clear_selection(self) -> None:
        """清除选区"""
        self._selection = None
    
    def select_range(self, start: int, length: int) -> None:
        """
        从起始位置选择指定长度
        
        Args:
            start: 起始位置
            length: 选择长度
        """
        self.set_selection(start, start + length)
    
    def select_all(self) -> None:
        """全选"""
        self.set_selection(0, self.length)
    
    # ==================== 文本编辑 ====================
    
    def insert_text(self, text: str, at_cursor: bool = True) -> None:
        """
        插入文本
        
        Args:
            text: 要插入的文本
            at_cursor: 是否在光标位置插入 (False 则在选区起始位置)
        """
        # 如果有选区，先删除选区内容
        if self._selection and not self._selection.is_empty:
            self.delete_selection()
        
        # 确定插入位置
        insert_pos = self._cursor if at_cursor else 0
        
        # 插入文本
        self._text = (self._text[:insert_pos] + 
                     text + 
                     self._text[insert_pos:])
        
        # 更新光标位置
        self._cursor = insert_pos + len(text)
        
        # 记录样式范围
        if self._current_style != TextStyle.NORMAL:
            self._style_ranges.append((insert_pos, len(text), self._current_style))
    
    def delete_char(self, forward: bool = False) -> bool:
        """
        删除单个字符
        
        Args:
            forward: True 为 Delete (删除光标后), False 为 Backspace (删除光标前)
        
        Returns:
            是否成功删除
        """
        # 如果有选区，删除选区
        if self._selection and not self._selection.is_empty:
            return self.delete_selection()
        
        # 确定删除位置
        if forward:
            if self._cursor >= self.length:
                return False
            delete_pos = self._cursor
        else:
            if self._cursor <= 0:
                return False
            delete_pos = self._cursor - 1
        
        # 删除字符
        self._text = self._text[:delete_pos] + self._text[delete_pos + 1:]
        
        # 更新光标
        if not forward:
            self._cursor -= 1
        
        return True
    
    def delete_selection(self) -> bool:
        """
        删除选区内容
        
        Returns:
            是否成功删除
        """
        if not self._selection or self._selection.is_empty:
            return False
        
        # 删除选区文本
        self._text = (self._text[:self._selection.start] + 
                     self._text[self._selection.end:])
        
        # 更新光标到选区起始位置
        self._cursor = self._selection.start
        
        # 清除选区
        self._selection = None
        
        return True
    
    def replace_text(self, start: int, end: int, new_text: str) -> None:
        """
        替换指定范围的文本
        
        Args:
            start: 起始位置
            end: 结束位置
            new_text: 新文本
        """
        start = max(0, min(start, self.length))
        end = max(start, min(end, self.length))
        
        self._text = self._text[:start] + new_text + self._text[end:]
        self._cursor = start + len(new_text)
        self._selection = None
    
    # ==================== 样式操作 ====================
    
    def set_style(self, style: TextStyle) -> None:
        """设置当前样式"""
        self._current_style = style
    
    def get_style_ranges(self) -> list[Tuple[int, int, TextStyle]]:
        """获取所有样式范围"""
        return self._style_ranges.copy()
    
    # ==================== 状态查询 ====================
    
    def get_state(self, timestamp: float = 0.0) -> EditorState:
        """
        获取当前完整状态快照
        
        Args:
            timestamp: 时间戳
            
        Returns:
            EditorState 对象
        """
        return EditorState(
            text=self._text,
            cursor_pos=self._cursor,
            selection=self._selection,
            current_style=self._current_style,
            timestamp=timestamp
        )
    
    def get_visible_text(self, before: int = 20, after: int = 20) -> str:
        """
        获取光标周围的可见文本（用于调试）
        
        Args:
            before: 光标前字符数
            after: 光标后字符数
        
        Returns:
            格式化的可见文本，用 | 标记光标位置
        """
        start = max(0, self._cursor - before)
        end = min(self.length, self._cursor + after)
        
        prefix = "..." if start > 0 else ""
        suffix = "..." if end < self.length else ""
        
        before_cursor = self._text[start:self._cursor]
        after_cursor = self._text[self._cursor:end]
        
        return f"{prefix}{before_cursor}|{after_cursor}{suffix}"
    
    def __repr__(self) -> str:
        return (f"TextBuffer(len={self.length}, cursor={self._cursor}, "
                f"selection={self._selection})")
