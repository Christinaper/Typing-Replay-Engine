"""
行为调度与时间控制 (Scheduler)
管理动作序列的回放和时间控制
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, Iterator
import time

from buffer import TextBuffer, EditorState
from actions import Action


@dataclass
class PlaybackEvent:
    """回放事件"""
    timestamp: float  # 相对开始时间（秒）
    action: Action
    state_before: EditorState
    state_after: EditorState
    
    def __repr__(self) -> str:
        return (f"PlaybackEvent(t={self.timestamp:.3f}s, "
                f"action={self.action.__class__.__name__})")


class PlaybackScheduler:
    """
    回放调度器
    管理动作序列的时间控制和执行
    """
    
    def __init__(self, buffer: Optional[TextBuffer] = None):
        """
        初始化调度器
        
        Args:
            buffer: 文本缓冲区（若为 None 则自动创建）
        """
        self.buffer = buffer or TextBuffer()
        self._actions: list[Action] = []
        self._events: list[PlaybackEvent] = []
        self._current_time: float = 0.0
        
        # 回调函数
        self._on_action_executed: Optional[Callable[[PlaybackEvent], None]] = None
        self._on_state_changed: Optional[Callable[[EditorState], None]] = None
    
    # ==================== 动作管理 ====================
    
    def add_action(self, action: Action) -> 'PlaybackScheduler':
        """
        添加动作到序列
        
        Args:
            action: 要添加的动作
        
        Returns:
            self (支持链式调用)
        """
        self._actions.append(action)
        return self
    
    def add_actions(self, actions: list[Action]) -> 'PlaybackScheduler':
        """
        批量添加动作
        
        Args:
            actions: 动作列表
        
        Returns:
            self (支持链式调用)
        """
        self._actions.extend(actions)
        return self
    
    def clear_actions(self) -> None:
        """清空所有动作"""
        self._actions.clear()
        self._events.clear()
        self._current_time = 0.0
    
    def get_total_duration(self) -> float:
        """计算总持续时间"""
        return sum(action.get_duration() for action in self._actions)
    
    # ==================== 回调设置 ====================
    
    def on_action_executed(self, callback: Callable[[PlaybackEvent], None]) -> 'PlaybackScheduler':
        """
        设置动作执行回调
        
        Args:
            callback: 回调函数，接收 PlaybackEvent 参数
        
        Returns:
            self (支持链式调用)
        """
        self._on_action_executed = callback
        return self
    
    def on_state_changed(self, callback: Callable[[EditorState], None]) -> 'PlaybackScheduler':
        """
        设置状态变化回调
        
        Args:
            callback: 回调函数，接收 EditorState 参数
        
        Returns:
            self (支持链式调用)
        """
        self._on_state_changed = callback
        return self
    
    # ==================== 回放控制 ====================
    
    def play(self, real_time: bool = False, speed: float = 1.0) -> list[PlaybackEvent]:
        """
        播放动作序列
        
        Args:
            real_time: 是否实时播放（按实际时间延迟）
            speed: 播放速度倍率 (仅在 real_time=True 时有效)
        
        Returns:
            所有回放事件列表
        """
        self._events.clear()
        self._current_time = 0.0
        
        playback_start = time.time()
        
        for action in self._actions:
            # 记录执行前状态
            state_before = self.buffer.get_state(self._current_time)
            
            # 执行动作
            action.execute(self.buffer)
            
            # 计算持续时间
            duration = action.get_duration()
            self._current_time += duration
            
            # 记录执行后状态
            state_after = self.buffer.get_state(self._current_time)
            
            # 创建事件
            event = PlaybackEvent(
                timestamp=self._current_time,
                action=action,
                state_before=state_before,
                state_after=state_after
            )
            self._events.append(event)
            
            # 触发回调
            if self._on_action_executed:
                self._on_action_executed(event)
            
            if self._on_state_changed:
                self._on_state_changed(state_after)
            
            # 实时延迟
            if real_time and duration > 0:
                adjusted_duration = duration / speed
                time.sleep(adjusted_duration)
        
        return self._events
    
    def play_with_frame_callback(
        self,
        frame_callback: Callable[[EditorState, float], None],
        fps: int = 30
    ) -> None:
        """
        以固定帧率播放，适合生成动画
        
        Args:
            frame_callback: 每帧回调函数，接收 (state, timestamp) 参数
            fps: 目标帧率
        """
        frame_duration = 1.0 / fps
        total_duration = self.get_total_duration()
        
        current_time = 0.0
        action_index = 0
        action_start_time = 0.0
        
        while current_time <= total_duration:
            # 执行到当前时间的所有动作
            while action_index < len(self._actions):
                action = self._actions[action_index]
                action_duration = action.get_duration()
                action_end_time = action_start_time + action_duration
                
                if action_end_time <= current_time:
                    # 动作已完成，执行它
                    action.execute(self.buffer)
                    action_index += 1
                    action_start_time = action_end_time
                else:
                    # 动作还未完成
                    break
            
            # 生成当前帧
            state = self.buffer.get_state(current_time)
            frame_callback(state, current_time)
            
            # 推进时间
            current_time += frame_duration
    
    def replay_events(self) -> Iterator[PlaybackEvent]:
        """
        迭代器方式重放已记录的事件
        
        Yields:
            PlaybackEvent
        """
        for event in self._events:
            yield event
    
    # ==================== 状态查询 ====================
    
    def get_events(self) -> list[PlaybackEvent]:
        """获取所有回放事件"""
        return self._events.copy()
    
    def get_current_state(self) -> EditorState:
        """获取当前状态"""
        return self.buffer.get_state(self._current_time)
    
    def get_state_at_time(self, timestamp: float) -> Optional[EditorState]:
        """
        获取指定时间点的状态
        
        Args:
            timestamp: 目标时间
        
        Returns:
            该时间点的状态，若不存在则返回 None
        """
        for event in self._events:
            if event.timestamp >= timestamp:
                return event.state_after
        return None
    
    def reset(self) -> None:
        """重置调度器和缓冲区"""
        self.buffer = TextBuffer()
        self._events.clear()
        self._current_time = 0.0
    
    # ==================== 统计信息 ====================
    
    def get_stats(self) -> dict:
        """
        获取回放统计信息
        
        Returns:
            包含统计数据的字典
        """
        if not self._events:
            return {
                'total_actions': len(self._actions),
                'total_duration': self.get_total_duration(),
                'events_recorded': 0
            }
        
        action_types = {}
        for action in self._actions:
            action_type = action.__class__.__name__
            action_types[action_type] = action_types.get(action_type, 0) + 1
        
        return {
            'total_actions': len(self._actions),
            'total_duration': self.get_total_duration(),
            'events_recorded': len(self._events),
            'action_types': action_types,
            'final_text_length': len(self.buffer.text),
            'final_cursor': self.buffer.cursor
        }
    
    def __repr__(self) -> str:
        return (f"PlaybackScheduler(actions={len(self._actions)}, "
                f"duration={self.get_total_duration():.2f}s)")


class InteractiveScheduler(PlaybackScheduler):
    """
    交互式调度器
    支持步进、暂停、继续等控制
    """
    
    def __init__(self, buffer: Optional[TextBuffer] = None):
        super().__init__(buffer)
        self._paused = False
        self._current_action_index = 0
    
    def step(self) -> Optional[PlaybackEvent]:
        """
        执行下一个动作
        
        Returns:
            生成的事件，若已结束则返回 None
        """
        if self._current_action_index >= len(self._actions):
            return None
        
        action = self._actions[self._current_action_index]
        
        # 记录状态
        state_before = self.buffer.get_state(self._current_time)
        action.execute(self.buffer)
        
        duration = action.get_duration()
        self._current_time += duration
        
        state_after = self.buffer.get_state(self._current_time)
        
        # 创建事件
        event = PlaybackEvent(
            timestamp=self._current_time,
            action=action,
            state_before=state_before,
            state_after=state_after
        )
        self._events.append(event)
        
        # 触发回调
        if self._on_action_executed:
            self._on_action_executed(event)
        
        if self._on_state_changed:
            self._on_state_changed(state_after)
        
        self._current_action_index += 1
        return event
    
    def step_back(self) -> bool:
        """
        回退一步（重新构建状态）
        
        Returns:
            是否成功回退
        """
        if self._current_action_index <= 0:
            return False
        
        # 重置缓冲区
        self.buffer = TextBuffer()
        self._current_action_index -= 1
        self._current_time = 0.0
        self._events.clear()
        
        # 重新执行到当前位置
        for i in range(self._current_action_index):
            action = self._actions[i]
            action.execute(self.buffer)
            duration = action.get_duration()
            self._current_time += duration
        
        return True
    
    def is_finished(self) -> bool:
        """是否已播放完毕"""
        return self._current_action_index >= len(self._actions)
    
    def get_progress(self) -> float:
        """
        获取播放进度
        
        Returns:
            进度百分比 (0.0-1.0)
        """
        if not self._actions:
            return 1.0
        return self._current_action_index / len(self._actions)
