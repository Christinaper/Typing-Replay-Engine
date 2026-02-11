"""
示例和测试
演示打字回放引擎的各种功能
"""

import time
from pathlib import Path

from buffer import TextBuffer, TextStyle
from actions import (
    type_text, pause, backspace, move_cursor, select,
    delete_selection, set_style, TypeTextAction, InsertTextAction
)
from scheduler import PlaybackScheduler, InteractiveScheduler
from script_parser import ScriptParser, ScriptBuilder, load_demo_script
from console import ConsoleRenderer, EventLogger, SimpleDisplay


def example_basic_typing():
    """示例 1: 基础打字"""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Typing")
    print("=" * 60 + "\n")
    
    scheduler = PlaybackScheduler()
    
    # 添加动作
    scheduler.add_actions([
        type_text("Hello, ", wpm=60),
        pause(0.5),
        type_text("World!", wpm=40),
        pause(0.3),
        InsertTextAction(" 🌍"),
    ])
    
    # 设置回调
    logger = EventLogger(verbose=False)
    scheduler.on_action_executed(logger.log_event)
    
    # 播放
    events = scheduler.play()
    
    # 显示结果
    SimpleDisplay.show_text(scheduler.get_current_state(), "Final Result")
    logger.print_summary()


def example_editing_with_backspace():
    """示例 2: 带退格的编辑"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Editing with Backspace")
    print("=" * 60 + "\n")
    
    scheduler = PlaybackScheduler()
    
    scheduler.add_actions([
        type_text("The quikc brown fox", wpm=80),
        pause(0.5),
        # 发现拼写错误，删除 "quikc"
        move_cursor(9),  # 移动到 "quikc" 后面
        backspace(5),  # 删除 "quikc"
        type_text("quick", wpm=60),
    ])
    
    # 播放
    scheduler.play()
    
    SimpleDisplay.show_text(scheduler.get_current_state())


def example_selection_and_replace():
    """示例 3: 选区和替换"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Selection and Replace")
    print("=" * 60 + "\n")
    
    scheduler = PlaybackScheduler()
    
    scheduler.add_actions([
        type_text("I love JavaScript!", wpm=70),
        pause(0.5),
        # 选择 "JavaScript" 并替换为 "Python"
        select(7, 17),  # 选择 "JavaScript"
        pause(0.3),
        type_text("Python", wpm=60),
    ])
    
    # 实时播放
    renderer = ConsoleRenderer()
    scheduler.on_state_changed(
        lambda state: renderer.render_state(state, clear_previous=True)
    )
    
    scheduler.play(real_time=True, speed=2.0)  # 2倍速播放
    
    print("\n")
    SimpleDisplay.show_text(scheduler.get_current_state())


def example_code_editing():
    """示例 4: 代码编辑"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Code Editing")
    print("=" * 60 + "\n")
    
    scheduler = PlaybackScheduler()
    
    # 模拟编写一个函数
    scheduler.add_actions([
        type_text("def calculate_sum(", wpm=80),
        pause(0.2),
        type_text("a, b", wpm=70),
        type_text("):", wpm=80),
        pause(0.3),
        type_text("\n    return a + b", wpm=75),
        pause(0.5),
        # 修改：改为 multiply
        move_cursor(4),
        select(4, 17),  # 选择 "calculate_sum"
        type_text("multiply", wpm=80),
        pause(0.3),
        move_cursor(-1, clear_selection=False),  # 移动到 "+"
        backspace(3),  # 删除 " + "
        type_text(" * ", wpm=60),
    ])
    
    scheduler.play()
    
    SimpleDisplay.show_text(scheduler.get_current_state())


def example_style_switching():
    """示例 5: 样式切换"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Style Switching")
    print("=" * 60 + "\n")
    
    scheduler = PlaybackScheduler()
    
    scheduler.add_actions([
        type_text("Normal text. ", wpm=60),
        set_style(TextStyle.BOLD),
        type_text("Bold text. ", wpm=60),
        set_style(TextStyle.ITALIC),
        type_text("Italic text. ", wpm=60),
        set_style(TextStyle.CODE),
        type_text("Code text.", wpm=60),
    ])
    
    scheduler.play()
    
    state = scheduler.get_current_state()
    SimpleDisplay.show_text(state)
    
    # 显示样式范围
    print("Style Ranges:")
    for start, length, style in scheduler.buffer.get_style_ranges():
        print(f"  [{start}:{start+length}] -> {style.value}")


def example_json_script():
    """示例 6: 从 JSON 脚本加载"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: JSON Script")
    print("=" * 60 + "\n")
    
    # 使用预设脚本
    actions = load_demo_script('code_editing')
    
    scheduler = PlaybackScheduler()
    scheduler.add_actions(actions)
    
    # 播放
    scheduler.play()
    
    SimpleDisplay.show_text(scheduler.get_current_state())
    print("\nScript Stats:", scheduler.get_stats())


def example_script_builder():
    """示例 7: 使用脚本构建器"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Script Builder")
    print("=" * 60 + "\n")
    
    # 使用构建器创建脚本
    builder = ScriptBuilder()
    builder.type("First line.", wpm=60) \
           .pause(0.5) \
           .type("\nSecond line.", wpm=70) \
           .pause(0.3) \
           .backspace(5) \
           .type("paragraph!", wpm=65)
    
    # 导出 JSON
    print("Generated Script:")
    print(builder.to_json())
    print()
    
    # 解析并播放
    actions = ScriptParser.parse(builder.build())
    scheduler = PlaybackScheduler()
    scheduler.add_actions(actions)
    scheduler.play()
    
    SimpleDisplay.show_text(scheduler.get_current_state())


def example_interactive_mode():
    """示例 8: 交互式模式（步进）"""
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Interactive Mode (Step-by-Step)")
    print("=" * 60 + "\n")
    
    scheduler = InteractiveScheduler()
    
    scheduler.add_actions([
        type_text("Step ", wpm=60),
        type_text("by ", wpm=60),
        type_text("step ", wpm=60),
        type_text("execution.", wpm=60),
    ])
    
    print("Stepping through actions...\n")
    
    step = 1
    while not scheduler.is_finished():
        event = scheduler.step()
        if event:
            print(f"Step {step}: {event.action}")
            print(f"  Text: '{scheduler.buffer.text}'")
            print(f"  Cursor: {scheduler.buffer.cursor}")
            print(f"  Progress: {scheduler.get_progress()*100:.1f}%")
            print()
            step += 1
    
    SimpleDisplay.show_text(scheduler.get_current_state(), "Final State")


def example_emoji_and_unicode():
    """示例 9: Emoji 和特殊字符"""
    print("\n" + "=" * 60)
    print("EXAMPLE 9: Emoji and Unicode")
    print("=" * 60 + "\n")
    
    scheduler = PlaybackScheduler()
    
    scheduler.add_actions([
        type_text("Coding is fun! ", wpm=60),
        InsertTextAction("💻"),
        pause(0.2),
        InsertTextAction("🚀"),
        pause(0.2),
        InsertTextAction("✨"),
        pause(0.5),
        type_text("\n你好世界！", wpm=50),
        pause(0.3),
        type_text("\nПривет мир!", wpm=50),
    ])
    
    scheduler.play()
    
    SimpleDisplay.show_text(scheduler.get_current_state())


def example_frame_based_export():
    """示例 10: 基于帧的导出"""
    print("\n" + "=" * 60)
    print("EXAMPLE 10: Frame-based Export (Animation)")
    print("=" * 60 + "\n")
    
    scheduler = PlaybackScheduler()
    
    scheduler.add_actions([
        type_text("Animated ", wpm=40),
        type_text("typing...", wpm=40),
    ])
    
    frames = []
    
    def capture_frame(state, timestamp):
        frames.append({
            'time': timestamp,
            'text': state.text,
            'cursor': state.cursor_pos
        })
    
    # 以 10 FPS 生成帧
    scheduler.play_with_frame_callback(capture_frame, fps=10)
    
    print(f"Generated {len(frames)} frames\n")
    print("Frame samples:")
    for i in range(0, len(frames), max(1, len(frames) // 5)):
        frame = frames[i]
        print(f"  Frame {i}: t={frame['time']:.2f}s, "
              f"text='{frame['text']}', cursor={frame['cursor']}")


def run_all_examples():
    """运行所有示例"""
    examples = [
        example_basic_typing,
        example_editing_with_backspace,
        example_selection_and_replace,
        example_code_editing,
        example_style_switching,
        example_json_script,
        example_script_builder,
        example_interactive_mode,
        example_emoji_and_unicode,
        example_frame_based_export,
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
            time.sleep(0.5)  # 短暂暂停，便于阅读
        except Exception as e:
            print(f"\n❌ Example {i} failed: {e}\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # 运行指定示例
        example_num = int(sys.argv[1])
        examples = [
            example_basic_typing,
            example_editing_with_backspace,
            example_selection_and_replace,
            example_code_editing,
            example_style_switching,
            example_json_script,
            example_script_builder,
            example_interactive_mode,
            example_emoji_and_unicode,
            example_frame_based_export,
        ]
        
        if 1 <= example_num <= len(examples):
            examples[example_num - 1]()
        else:
            print(f"Example {example_num} not found. Available: 1-{len(examples)}")
    else:
        # 运行所有示例
        run_all_examples()
