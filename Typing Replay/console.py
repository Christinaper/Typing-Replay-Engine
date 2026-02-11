"""
控制台输出工具
用于可视化回放过程
"""

import sys
from typing import Optional
from datetime import timedelta

from buffer import EditorState, TextStyle
from scheduler import PlaybackEvent


class ConsoleRenderer:
    """控制台渲染器"""
    
    def __init__(self, show_cursor: bool = True, show_selection: bool = True):
        """
        初始化渲染器
        
        Args:
            show_cursor: 是否显示光标
            show_selection: 是否显示选区
        """
        self.show_cursor = show_cursor
        self.show_selection = show_selection
        self._last_line_count = 0
    
    def render_state(self, state: EditorState, clear_previous: bool = False) -> None:
        """
        渲染编辑器状态
        
        Args:
            state: 编辑器状态
            clear_previous: 是否清除之前的输出
        """
        if clear_previous:
            self.clear_lines(self._last_line_count)
        
        lines = []
        
        # 标题
        lines.append("=" * 60)
        lines.append(f"Time: {state.timestamp:.3f}s | "
                    f"Cursor: {state.cursor_pos} | "
                    f"Length: {len(state.text)} | "
                    f"Style: {state.current_style.value}")
        lines.append("-" * 60)
        
        # 文本内容（带光标和选区标记）
        text_lines = self._format_text(state)
        lines.extend(text_lines)
        
        lines.append("=" * 60)
        
        # 输出
        output = '\n'.join(lines)
        print(output, flush=True)
        
        self._last_line_count = len(lines)
    
    def _format_text(self, state: EditorState) -> list[str]:
        """格式化文本，添加光标和选区标记"""
        text = state.text
        cursor = state.cursor_pos
        selection = state.selection
        
        if not text:
            return ["(empty)" if not self.show_cursor else "|"]
        
        # 分行显示
        lines = text.split('\n')
        result = []
        char_pos = 0
        
        for line_idx, line in enumerate(lines):
            line_start = char_pos
            line_end = char_pos + len(line)
            
            # 构建带标记的行
            marked_line = ""
            
            for i, char in enumerate(line):
                abs_pos = line_start + i
                
                # 检查是否在选区内
                in_selection = False
                if self.show_selection and selection and not selection.is_empty:
                    in_selection = selection.start <= abs_pos < selection.end
                
                # 检查是否是光标位置
                is_cursor = self.show_cursor and abs_pos == cursor
                
                # 添加字符（带标记）
                if in_selection:
                    marked_line += f"[{char}]"
                else:
                    marked_line += char
                
                # 添加光标
                if is_cursor:
                    marked_line += "|"
            
            # 行尾光标
            if self.show_cursor and cursor == line_end:
                marked_line += "|"
            
            result.append(marked_line if marked_line else "(empty line)")
            
            # 移动到下一行（包括换行符）
            char_pos = line_end + 1
        
        return result
    
    def render_event(self, event: PlaybackEvent) -> None:
        """
        渲染回放事件
        
        Args:
            event: 回放事件
        """
        print(f"\n[{event.timestamp:.3f}s] {event.action}")
        self.render_state(event.state_after)
    
    def render_progress(self, current: int, total: int, duration: float) -> None:
        """
        渲染进度条
        
        Args:
            current: 当前进度
            total: 总数
            duration: 当前持续时间
        """
        if total == 0:
            return
        
        progress = current / total
        bar_width = 40
        filled = int(bar_width * progress)
        bar = "█" * filled + "░" * (bar_width - filled)
        
        time_str = str(timedelta(seconds=int(duration)))
        
        sys.stdout.write(f"\r[{bar}] {current}/{total} ({progress*100:.1f}%) | {time_str}")
        sys.stdout.flush()
    
    @staticmethod
    def clear_lines(count: int) -> None:
        """清除指定行数"""
        for _ in range(count):
            sys.stdout.write("\033[F\033[K")  # 上移并清除行
        sys.stdout.flush()


class EventLogger:
    """事件日志记录器"""
    
    def __init__(self, verbose: bool = True):
        """
        初始化日志记录器
        
        Args:
            verbose: 是否详细输出
        """
        self.verbose = verbose
        self.events = []
    
    def log_event(self, event: PlaybackEvent) -> None:
        """记录事件"""
        self.events.append(event)
        
        if self.verbose:
            action_name = event.action.__class__.__name__
            print(f"[{event.timestamp:.3f}s] {action_name}: "
                  f"{event.state_before.cursor_pos} -> {event.state_after.cursor_pos}")
    
    def log_state(self, state: EditorState) -> None:
        """记录状态"""
        if self.verbose:
            preview = state.text[:50] + "..." if len(state.text) > 50 else state.text
            print(f"State @ {state.timestamp:.3f}s: '{preview}' "
                  f"(cursor={state.cursor_pos})")
    
    def get_summary(self) -> dict:
        """获取日志摘要"""
        if not self.events:
            return {'total_events': 0}
        
        action_counts = {}
        for event in self.events:
            action_type = event.action.__class__.__name__
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        return {
            'total_events': len(self.events),
            'total_duration': self.events[-1].timestamp if self.events else 0,
            'action_counts': action_counts,
            'final_text_length': len(self.events[-1].state_after.text) if self.events else 0
        }
    
    def print_summary(self) -> None:
        """打印摘要"""
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print("PLAYBACK SUMMARY")
        print("=" * 60)
        print(f"Total Events: {summary['total_events']}")
        print(f"Total Duration: {summary.get('total_duration', 0):.3f}s")
        print(f"Final Text Length: {summary.get('final_text_length', 0)} chars")
        
        if 'action_counts' in summary:
            print("\nAction Breakdown:")
            for action_type, count in sorted(summary['action_counts'].items()):
                print(f"  {action_type}: {count}")
        
        print("=" * 60)


class SimpleDisplay:
    """简单文本显示（仅显示最终结果）"""
    
    @staticmethod
    def show_text(state: EditorState, title: str = "Current Text") -> None:
        """
        显示文本状态
        
        Args:
            state: 编辑器状态
            title: 标题
        """
        print(f"\n{'=' * 60}")
        print(f"{title} (t={state.timestamp:.3f}s)")
        print(f"{'=' * 60}")
        print(state.text)
        print(f"{'=' * 60}")
        print(f"Cursor: {state.cursor_pos} | Length: {len(state.text)} | "
              f"Style: {state.current_style.value}")
        if state.selection:
            print(f"Selection: [{state.selection.start}:{state.selection.end}]")
        print(f"{'=' * 60}\n")
    
    @staticmethod
    def show_diff(before: EditorState, after: EditorState) -> None:
        """
        显示状态差异
        
        Args:
            before: 之前的状态
            after: 之后的状态
        """
        print(f"\n{'=' * 60}")
        print(f"BEFORE (t={before.timestamp:.3f}s):")
        print(f"{'=' * 60}")
        print(before.text)
        print(f"\n{'=' * 60}")
        print(f"AFTER (t={after.timestamp:.3f}s):")
        print(f"{'=' * 60}")
        print(after.text)
        print(f"\n{'=' * 60}")
        print(f"Changes: {len(before.text)} -> {len(after.text)} chars")
        print(f"Cursor: {before.cursor_pos} -> {after.cursor_pos}")
        print(f"{'=' * 60}\n")
