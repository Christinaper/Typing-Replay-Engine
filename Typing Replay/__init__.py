"""
Typing Replay Engine
参数驱动的打字回放引擎

主入口和便捷 API
"""

__version__ = '1.0.0'
__author__ = 'Claude'

# 导出核心类
from buffer import TextBuffer, Selection, TextStyle, EditorState
from actions import (
    Action,
    TypeTextAction, InsertTextAction, BackspaceAction, DeleteAction,
    MoveCursorAction, SetSelectionAction, DeleteSelectionAction,
    SetStyleAction, PauseAction, ReplaceTextAction,
    type_text, pause, backspace, move_cursor, select, delete_selection, set_style
)
from scheduler import PlaybackScheduler, InteractiveScheduler, PlaybackEvent
from script_parser import ScriptParser, ScriptBuilder, load_demo_script
from console import ConsoleRenderer, EventLogger, SimpleDisplay


# 便捷 API
def create_replay(actions=None):
    """
    创建回放调度器的便捷函数
    
    Args:
        actions: 动作列表或脚本（可选）
    
    Returns:
        PlaybackScheduler
    """
    scheduler = PlaybackScheduler()
    
    if actions is not None:
        # 检查是否是 Action 对象列表
        if isinstance(actions, list) and len(actions) > 0 and isinstance(actions[0], Action):
            # 直接是动作列表
            scheduler.add_actions(actions)
        elif isinstance(actions, (dict, str)):
            # 解析脚本
            parsed_actions = ScriptParser.parse(actions)
            scheduler.add_actions(parsed_actions)
        elif isinstance(actions, list):
            # 尝试解析为脚本
            parsed_actions = ScriptParser.parse(actions)
            scheduler.add_actions(parsed_actions)
        else:
            # 单个 Action
            scheduler.add_action(actions)
    
    return scheduler


def quick_play(script, real_time=False, show_output=True):
    """
    快速播放脚本的便捷函数
    
    Args:
        script: 脚本（字典、列表或动作）
        real_time: 是否实时播放
        show_output: 是否显示输出
    
    Returns:
        最终文本
    """
    scheduler = create_replay(script)
    
    if show_output:
        display = SimpleDisplay()
        scheduler.on_state_changed(
            lambda state: display.show_text(state, "Current State")
        )
    
    scheduler.play(real_time=real_time)
    
    return scheduler.buffer.text


def load_and_play(filepath, real_time=False):
    """
    从文件加载并播放脚本
    
    Args:
        filepath: 脚本文件路径
        real_time: 是否实时播放
    
    Returns:
        PlaybackScheduler
    """
    actions = ScriptParser.parse(filepath)
    scheduler = create_replay(actions)
    scheduler.play(real_time=real_time)
    
    return scheduler


# 导出所有公共 API
__all__ = [
    # 版本信息
    '__version__',
    
    # 核心类
    'TextBuffer', 'Selection', 'TextStyle', 'EditorState',
    'Action', 'PlaybackScheduler', 'InteractiveScheduler', 'PlaybackEvent',
    'ScriptParser', 'ScriptBuilder',
    'ConsoleRenderer', 'EventLogger', 'SimpleDisplay',
    
    # 动作类
    'TypeTextAction', 'InsertTextAction', 'BackspaceAction', 'DeleteAction',
    'MoveCursorAction', 'SetSelectionAction', 'DeleteSelectionAction',
    'SetStyleAction', 'PauseAction', 'ReplaceTextAction',
    
    # 便捷函数
    'type_text', 'pause', 'backspace', 'move_cursor', 'select', 
    'delete_selection', 'set_style',
    'create_replay', 'quick_play', 'load_and_play', 'load_demo_script',
]


if __name__ == '__main__':
    # 简单演示
    print(f"Typing Replay Engine v{__version__}")
    print("=" * 60)
    
    # 运行一个简单的演示
    scheduler = create_replay([
        type_text("Welcome to Typing Replay Engine!", wpm=60),
        pause(0.5),
        type_text("\nThis is a demo.", wpm=50)
    ])
    
    scheduler.play()
    
    print("\nFinal Text:")
    print("-" * 60)
    print(scheduler.buffer.text)
    print("-" * 60)
    
    print(f"\nTotal Duration: {scheduler.get_total_duration():.2f}s")
    print(f"Total Actions: {len(scheduler._actions)}")
    
    print("\nFor more examples, run: python examples.py")
    print("For tests, run: python test_engine.py")
