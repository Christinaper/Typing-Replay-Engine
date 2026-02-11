"""
新功能测试与演示
测试逐字打字、逐字删除、光标闪烁和 emoji 快捷码
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from actions import TypeTextAction, BackspaceAction, type_text, pause, expand_emoji_shortcuts, EMOJI_SHORTCUTS
from scheduler import PlaybackScheduler
from buffer import TextBuffer
import time


def test_emoji_shortcuts():
    """测试 emoji 快捷码"""
    print("\n" + "="*60)
    print("测试 1: Emoji 快捷码展开")
    print("="*60)
    
    test_cases = [
        "Hello :smile: World!",
        "I :heart: Python :rocket:",
        "Good job :clap: :100: :fire:",
        ":warning: Be careful :exclamation:",
    ]
    
    for text in test_cases:
        expanded = expand_emoji_shortcuts(text)
        print(f"输入: {text}")
        print(f"输出: {expanded}")
        print()
    
    print(f"\n可用的 emoji 快捷码总数: {len(EMOJI_SHORTCUTS)}")
    print("\n常用快捷码示例:")
    common = [':smile:', ':heart:', ':rocket:', ':fire:', ':check:', ':100:']
    for shortcut in common:
        print(f"  {shortcut:15s} → {EMOJI_SHORTCUTS[shortcut]}")


def test_char_by_char_typing():
    """测试逐字打字效果"""
    print("\n" + "="*60)
    print("测试 2: 逐字打字效果")
    print("="*60)
    
    buffer = TextBuffer()
    action = TypeTextAction("Hello, World!", avg_char_delay=0.1)
    
    print(f"文本: '{action.text}'")
    print(f"字符数: {len(action.text)}")
    print(f"预计时长: {action.get_duration():.2f}秒")
    print("\n模拟逐字打字:")
    
    # 模拟逐字符执行
    for i in range(len(action.text)):
        buffer.insert_text(action.text[i])
        print(f"  [{i+1:2d}] {buffer.text}")
        time.sleep(0.05)  # 快速演示
    
    print("\n✓ 逐字打字测试完成")


def test_backspace_effect():
    """测试逐字删除效果"""
    print("\n" + "="*60)
    print("测试 3: 逐字删除效果")
    print("="*60)
    
    buffer = TextBuffer()
    buffer.insert_text("Hello, World!")
    
    print(f"初始文本: '{buffer.text}'")
    print(f"删除 6 个字符:")
    
    action = BackspaceAction(count=6)
    
    # 模拟逐步删除
    for i in range(6):
        buffer.delete_char(forward=False)
        print(f"  [{i+1}] {buffer.text}")
        time.sleep(0.05)
    
    print(f"\n最终文本: '{buffer.text}'")
    print("✓ 逐字删除测试完成")


def test_emoji_in_typing():
    """测试打字中的 emoji"""
    print("\n" + "="*60)
    print("测试 4: 打字中使用 Emoji 快捷码")
    print("="*60)
    
    buffer = TextBuffer()
    
    # 使用快捷码
    action = TypeTextAction("Coding is fun :rocket: :fire:", avg_char_delay=0.08)
    
    print(f"原始输入: 'Coding is fun :rocket: :fire:'")
    print(f"展开后: '{action.text}'")
    print(f"字符数: {len(action.text)}")
    print("\n逐字打字:")
    
    for i in range(len(action.text)):
        buffer.insert_text(action.text[i])
        if i % 3 == 0:  # 每3个字符显示一次
            print(f"  {buffer.text}")
        time.sleep(0.03)
    
    print(f"\n最终: {buffer.text}")
    print("✓ Emoji 打字测试完成")


def demo_complete_workflow():
    """完整工作流演示"""
    print("\n" + "="*60)
    print("演示 5: 完整打字回放工作流")
    print("="*60)
    
    scheduler = PlaybackScheduler()
    
    # 创建一个完整的脚本
    scheduler.add_actions([
        type_text("Hello :smile:", wpm=60),
        pause(0.5),
        type_text("\nThis is a test.", wpm=70),
        pause(0.3),
        BackspaceAction(count=5),
        pause(0.2),
        type_text("demo! :rocket:", wpm=60),
    ])
    
    print(f"动作数量: {len(scheduler._actions)}")
    print(f"预计时长: {scheduler.get_total_duration():.2f}秒")
    print("\n执行脚本（快速模式）...")
    
    # 非实时播放（快速）
    events = scheduler.play()
    
    print(f"\n最终文本:")
    print("-" * 40)
    print(scheduler.buffer.text)
    print("-" * 40)
    print("\n✓ 完整工作流演示完成")


def show_emoji_reference():
    """显示 emoji 参考表"""
    print("\n" + "="*60)
    print("Emoji 快捷码完整参考")
    print("="*60)
    
    categories = {
        '表情': [':smile:', ':grin:', ':laugh:', ':wink:', ':heart:', ':cry:', ':sad:', ':angry:', ':cool:', ':think:'],
        '手势': [':like:', ':muscle:', ':pray:', ':clap:', ':wave:', ':eye:', ':100:', ':ok:', ':point:', ':hand:'],
        '符号': [':fire:', ':star:', ':check:', ':cross:', ':rocket:', ':party:', ':sparkles:', ':tada:'],
        '食物': [':coffee:', ':pizza:', ':beer:', ':cake:'],
        '物品': [':gift:', ':book:', ':pen:', ':mail:', ':phone:', ':computer:', ':bulb:', ':lock:', ':key:'],
        '天气': [':sun:', ':moon:', ':cloud:', ':rain:', ':snow:'],
        '自然': [':tree:', ':flower:', ':rose:', ':cat:', ':dog:', ':bird:', ':fish:'],
        '其他': [':warning:', ':info:', ':question:', ':exclamation:'],
    }
    
    for category, shortcuts in categories.items():
        print(f"\n{category}:")
        for shortcut in shortcuts:
            emoji = EMOJI_SHORTCUTS.get(shortcut, '?')
            print(f"  {shortcut:15s} {emoji}")
    
    print(f"\n总计: {len(EMOJI_SHORTCUTS)} 个快捷码")


def create_demo_json():
    """创建演示 JSON 脚本"""
    import json
    
    demo = {
        "actions": [
            {"type": "type", "text": "Hello :smile: Welcome!", "wpm": 60},
            {"type": "pause", "duration": 0.5},
            {"type": "type", "text": "\nLet me show you something :point:", "wpm": 65},
            {"type": "pause", "duration": 0.8},
            {"type": "type", "text": "\nCoding is :fire: :rocket: :100:", "wpm": 70},
            {"type": "pause", "duration": 0.5},
            {"type": "backspace", "count": 7},
            {"type": "type", "text": "awesome! :heart:", "wpm": 60}
        ]
    }
    
    with open('emoji_demo.json', 'w', encoding='utf-8') as f:
        json.dump(demo, f, indent=2, ensure_ascii=False)
    
    print("\n✓ 已创建 emoji_demo.json")
    print("  可以在 GUI 中打开此文件查看效果")


def main():
    """运行所有测试"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║        Typing Replay Engine - 新功能测试                  ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    tests = [
        ("Emoji 快捷码展开", test_emoji_shortcuts),
        ("逐字打字效果", test_char_by_char_typing),
        ("逐字删除效果", test_backspace_effect),
        ("Emoji 打字集成", test_emoji_in_typing),
        ("完整工作流", demo_complete_workflow),
    ]
    
    for i, (name, test_func) in enumerate(tests, 1):
        try:
            test_func()
            time.sleep(0.5)
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
    
    # 显示参考信息
    show_emoji_reference()
    
    # 创建演示文件
    create_demo_json()
    
    print("\n" + "="*60)
    print("所有测试完成！")
    print("="*60)
    print("\n下一步:")
    print("  1. 运行 'python gui.py' 启动 GUI")
    print("  2. 打开 'emoji_demo.json' 查看 emoji 效果")
    print("  3. 观察逐字打字和删除的动画效果")
    print("  4. 注意光标闪烁效果")
    print("\n")


if __name__ == '__main__':
    main()
