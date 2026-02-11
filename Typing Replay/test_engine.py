"""
单元测试
测试打字回放引擎的核心功能
"""

import unittest
from buffer import TextBuffer, Selection, TextStyle
from actions import (
    TypeTextAction, BackspaceAction, MoveCursorAction,
    SetSelectionAction, DeleteSelectionAction, type_text, pause
)
from scheduler import PlaybackScheduler, InteractiveScheduler
from script_parser import ScriptParser, ScriptBuilder


class TestTextBuffer(unittest.TestCase):
    """测试文本缓冲区"""
    
    def setUp(self):
        self.buffer = TextBuffer()
    
    def test_initial_state(self):
        """测试初始状态"""
        self.assertEqual(self.buffer.text, "")
        self.assertEqual(self.buffer.cursor, 0)
        self.assertIsNone(self.buffer.selection)
        self.assertEqual(self.buffer.length, 0)
    
    def test_insert_text(self):
        """测试插入文本"""
        self.buffer.insert_text("Hello")
        self.assertEqual(self.buffer.text, "Hello")
        self.assertEqual(self.buffer.cursor, 5)
        
        self.buffer.insert_text(" World")
        self.assertEqual(self.buffer.text, "Hello World")
        self.assertEqual(self.buffer.cursor, 11)
    
    def test_move_cursor(self):
        """测试光标移动"""
        self.buffer.insert_text("Hello")
        
        self.buffer.move_cursor(0)
        self.assertEqual(self.buffer.cursor, 0)
        
        self.buffer.move_cursor(3)
        self.assertEqual(self.buffer.cursor, 3)
        
        # 超出范围应被限制
        self.buffer.move_cursor(100)
        self.assertEqual(self.buffer.cursor, 5)
        
        self.buffer.move_cursor(-10)
        self.assertEqual(self.buffer.cursor, 0)
    
    def test_move_cursor_relative(self):
        """测试相对光标移动"""
        self.buffer.insert_text("Hello")
        self.buffer.move_cursor(0)
        
        self.buffer.move_cursor_relative(2)
        self.assertEqual(self.buffer.cursor, 2)
        
        self.buffer.move_cursor_relative(-1)
        self.assertEqual(self.buffer.cursor, 1)
    
    def test_backspace(self):
        """测试退格删除"""
        self.buffer.insert_text("Hello")
        
        self.assertTrue(self.buffer.delete_char(forward=False))
        self.assertEqual(self.buffer.text, "Hell")
        self.assertEqual(self.buffer.cursor, 4)
        
        # 在开头时不能删除
        self.buffer.move_cursor(0)
        self.assertFalse(self.buffer.delete_char(forward=False))
        self.assertEqual(self.buffer.text, "Hell")
    
    def test_delete(self):
        """测试 Delete 键"""
        self.buffer.insert_text("Hello")
        self.buffer.move_cursor(0)
        
        self.assertTrue(self.buffer.delete_char(forward=True))
        self.assertEqual(self.buffer.text, "ello")
        self.assertEqual(self.buffer.cursor, 0)
    
    def test_selection(self):
        """测试选区"""
        self.buffer.insert_text("Hello World")
        
        self.buffer.set_selection(0, 5)
        self.assertIsNotNone(self.buffer.selection)
        self.assertEqual(self.buffer.selection.start, 0)
        self.assertEqual(self.buffer.selection.end, 5)
        self.assertEqual(self.buffer.selection.length, 5)
        
        # 选区自动排序
        self.buffer.set_selection(10, 6)
        self.assertEqual(self.buffer.selection.start, 6)
        self.assertEqual(self.buffer.selection.end, 10)
    
    def test_delete_selection(self):
        """测试删除选区"""
        self.buffer.insert_text("Hello World")
        self.buffer.set_selection(0, 5)
        
        self.assertTrue(self.buffer.delete_selection())
        self.assertEqual(self.buffer.text, " World")
        self.assertEqual(self.buffer.cursor, 0)
        self.assertIsNone(self.buffer.selection)
    
    def test_insert_with_selection(self):
        """测试在有选区时插入文本"""
        self.buffer.insert_text("Hello World")
        self.buffer.set_selection(0, 5)
        
        self.buffer.insert_text("Hi")
        self.assertEqual(self.buffer.text, "Hi World")
        self.assertEqual(self.buffer.cursor, 2)
    
    def test_replace_text(self):
        """测试替换文本"""
        self.buffer.insert_text("Hello World")
        self.buffer.replace_text(6, 11, "Python")
        
        self.assertEqual(self.buffer.text, "Hello Python")
        self.assertEqual(self.buffer.cursor, 12)


class TestActions(unittest.TestCase):
    """测试动作"""
    
    def setUp(self):
        self.buffer = TextBuffer()
    
    def test_type_text_action(self):
        """测试打字动作"""
        action = TypeTextAction("Hello", avg_char_delay=0.1)
        action.execute(self.buffer)
        
        self.assertEqual(self.buffer.text, "Hello")
        self.assertGreater(action.get_duration(), 0)
    
    def test_backspace_action(self):
        """测试退格动作"""
        self.buffer.insert_text("Hello")
        
        action = BackspaceAction(count=2)
        action.execute(self.buffer)
        
        self.assertEqual(self.buffer.text, "Hel")
        self.assertEqual(action.get_duration(), 0.1)  # 2 * 0.05
    
    def test_move_cursor_action(self):
        """测试光标移动动作"""
        self.buffer.insert_text("Hello")
        
        # 绝对位置
        action = MoveCursorAction(position=2)
        action.execute(self.buffer)
        self.assertEqual(self.buffer.cursor, 2)
        
        # 相对偏移
        action = MoveCursorAction(offset=1)
        action.execute(self.buffer)
        self.assertEqual(self.buffer.cursor, 3)
    
    def test_selection_action(self):
        """测试选区动作"""
        self.buffer.insert_text("Hello World")
        
        action = SetSelectionAction(0, 5)
        action.execute(self.buffer)
        
        self.assertIsNotNone(self.buffer.selection)
        self.assertEqual(self.buffer.selection.start, 0)
        self.assertEqual(self.buffer.selection.end, 5)
    
    def test_delete_selection_action(self):
        """测试删除选区动作"""
        self.buffer.insert_text("Hello World")
        self.buffer.set_selection(6, 11)
        
        action = DeleteSelectionAction()
        action.execute(self.buffer)
        
        self.assertEqual(self.buffer.text, "Hello ")
        self.assertIsNone(self.buffer.selection)


class TestScheduler(unittest.TestCase):
    """测试调度器"""
    
    def test_add_actions(self):
        """测试添加动作"""
        scheduler = PlaybackScheduler()
        
        scheduler.add_action(type_text("Hello"))
        scheduler.add_action(pause(0.5))
        
        self.assertEqual(len(scheduler._actions), 2)
    
    def test_play(self):
        """测试播放"""
        scheduler = PlaybackScheduler()
        
        scheduler.add_actions([
            type_text("Hello", wpm=60),
            pause(0.5),
            type_text(" World", wpm=60)
        ])
        
        events = scheduler.play()
        
        self.assertEqual(len(events), 3)
        self.assertEqual(scheduler.buffer.text, "Hello World")
    
    def test_callbacks(self):
        """测试回调"""
        scheduler = PlaybackScheduler()
        
        executed_events = []
        state_changes = []
        
        scheduler.on_action_executed(lambda e: executed_events.append(e))
        scheduler.on_state_changed(lambda s: state_changes.append(s))
        
        scheduler.add_actions([
            type_text("Test", wpm=60),
            pause(0.5)
        ])
        
        scheduler.play()
        
        self.assertEqual(len(executed_events), 2)
        self.assertEqual(len(state_changes), 2)
    
    def test_interactive_scheduler(self):
        """测试交互式调度器"""
        scheduler = InteractiveScheduler()
        
        scheduler.add_actions([
            type_text("A", wpm=60),
            type_text("B", wpm=60),
            type_text("C", wpm=60)
        ])
        
        # 步进
        event1 = scheduler.step()
        self.assertEqual(scheduler.buffer.text, "A")
        self.assertEqual(scheduler.get_progress(), 1/3)
        
        event2 = scheduler.step()
        self.assertEqual(scheduler.buffer.text, "AB")
        
        # 回退
        self.assertTrue(scheduler.step_back())
        self.assertEqual(scheduler.buffer.text, "A")
        
        # 完成
        scheduler.step()
        scheduler.step()
        self.assertTrue(scheduler.is_finished())


class TestScriptParser(unittest.TestCase):
    """测试脚本解析器"""
    
    def test_parse_dict(self):
        """测试解析字典"""
        script = {
            'actions': [
                {'type': 'type', 'text': 'Hello', 'wpm': 60},
                {'type': 'pause', 'duration': 0.5},
                {'type': 'backspace', 'count': 1}
            ]
        }
        
        actions = ScriptParser.parse(script)
        
        self.assertEqual(len(actions), 3)
        self.assertIsInstance(actions[0], TypeTextAction)
        self.assertEqual(actions[0].text, 'Hello')
    
    def test_parse_json_string(self):
        """测试解析 JSON 字符串"""
        json_str = '''
        {
            "actions": [
                {"type": "type", "text": "Test", "wpm": 50}
            ]
        }
        '''
        
        actions = ScriptParser.parse(json_str)
        
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].text, 'Test')
    
    def test_script_builder(self):
        """测试脚本构建器"""
        builder = ScriptBuilder()
        builder.type("Hello", wpm=60) \
               .pause(0.5) \
               .backspace(1)
        
        script = builder.build()
        
        self.assertEqual(len(script['actions']), 3)
        self.assertEqual(script['actions'][0]['type'], 'type')
        self.assertEqual(script['actions'][0]['text'], 'Hello')


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 创建脚本
        builder = ScriptBuilder()
        builder.type("Hello World", wpm=60) \
               .pause(0.5) \
               .select(0, 5) \
               .type("Hi", wpm=60)
        
        # 解析
        actions = ScriptParser.parse(builder.build())
        
        # 执行
        scheduler = PlaybackScheduler()
        scheduler.add_actions(actions)
        events = scheduler.play()
        
        # 验证结果
        self.assertEqual(scheduler.buffer.text, "Hi World")
        self.assertGreater(len(events), 0)
    
    def test_emoji_handling(self):
        """测试 Emoji 处理"""
        scheduler = PlaybackScheduler()
        scheduler.add_actions([
            type_text("Hello ", wpm=60),
            TypeTextAction("🌍", avg_char_delay=0.1)
        ])
        
        scheduler.play()
        self.assertEqual(scheduler.buffer.text, "Hello 🌍")
    
    def test_multiline_text(self):
        """测试多行文本"""
        scheduler = PlaybackScheduler()
        scheduler.add_action(type_text("Line 1\nLine 2\nLine 3", wpm=60))
        
        scheduler.play()
        self.assertEqual(scheduler.buffer.text.count('\n'), 2)


def run_tests():
    """运行所有测试"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
