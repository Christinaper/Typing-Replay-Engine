"""
脚本格式解析器
支持从 JSON / Python dict 加载动作序列
"""

import json
from typing import Any, Union
from pathlib import Path

from actions import (
    Action, TypeTextAction, InsertTextAction, BackspaceAction,
    DeleteAction, ReplaceTextAction, MoveCursorAction, SetSelectionAction,
    SelectRangeAction, ClearSelectionAction, DeleteSelectionAction,
    SetStyleAction, PauseAction, CompositeAction,
    type_text, pause, backspace
)
from buffer import TextStyle


class ScriptParser:
    """脚本解析器"""
    
    # 动作类型映射
    ACTION_TYPES = {
        'type': 'parse_type_text',
        'type_text': 'parse_type_text',
        'insert': 'parse_insert_text',
        'insert_text': 'parse_insert_text',
        'backspace': 'parse_backspace',
        'delete': 'parse_delete',
        'replace': 'parse_replace_text',
        'replace_text': 'parse_replace_text',
        'move_cursor': 'parse_move_cursor',
        'cursor': 'parse_move_cursor',
        'select': 'parse_set_selection',
        'selection': 'parse_set_selection',
        'select_range': 'parse_select_range',
        'clear_selection': 'parse_clear_selection',
        'delete_selection': 'parse_delete_selection',
        'set_style': 'parse_set_style',
        'style': 'parse_set_style',
        'pause': 'parse_pause',
        'wait': 'parse_pause',
        'composite': 'parse_composite',
        'group': 'parse_composite',
    }
    
    @classmethod
    def parse(cls, script: Union[str, dict, list, Path]) -> list[Action]:
        """
        解析脚本
        
        Args:
            script: 可以是：
                - JSON 字符串
                - Python 字典
                - 动作列表
                - 文件路径
        
        Returns:
            动作列表
        """
        # 处理文件路径
        if isinstance(script, (str, Path)):
            path = Path(script)
            if path.exists() and path.is_file():
                with open(path, 'r', encoding='utf-8') as f:
                    script = json.load(f)
            elif isinstance(script, str) and script.strip().startswith('{'):
                # JSON 字符串
                script = json.loads(script)
            else:
                raise ValueError(f"Invalid script: {script}")
        
        # 处理字典格式
        if isinstance(script, dict):
            if 'actions' in script:
                return cls.parse_actions(script['actions'])
            else:
                # 单个动作
                return [cls.parse_action(script)]
        
        # 处理列表格式
        if isinstance(script, list):
            return cls.parse_actions(script)
        
        raise ValueError(f"Unsupported script format: {type(script)}")
    
    @classmethod
    def parse_actions(cls, actions_data: list) -> list[Action]:
        """解析动作列表"""
        return [cls.parse_action(action_data) for action_data in actions_data]
    
    @classmethod
    def parse_action(cls, action_data: dict) -> Action:
        """解析单个动作"""
        if 'type' not in action_data:
            raise ValueError(f"Action must have 'type' field: {action_data}")
        
        action_type = action_data['type'].lower()
        
        if action_type not in cls.ACTION_TYPES:
            raise ValueError(f"Unknown action type: {action_type}")
        
        parser_method = getattr(cls, cls.ACTION_TYPES[action_type])
        return parser_method(action_data)
    
    # ==================== 解析器方法 ====================
    
    @staticmethod
    def parse_type_text(data: dict) -> TypeTextAction:
        """解析打字动作"""
        text = data.get('text', '')
        
        # 支持 wpm 参数
        if 'wpm' in data:
            wpm = data['wpm']
            chars_per_second = (wpm * 5) / 60
            avg_delay = 1.0 / chars_per_second
        else:
            avg_delay = data.get('avg_char_delay', 0.1)
        
        delay_variance = data.get('delay_variance', avg_delay * 0.3)
        
        return TypeTextAction(text, avg_delay, delay_variance)
    
    @staticmethod
    def parse_insert_text(data: dict) -> InsertTextAction:
        """解析即时插入动作"""
        return InsertTextAction(
            text=data.get('text', ''),
            duration=data.get('duration', 0.05)
        )
    
    @staticmethod
    def parse_backspace(data: dict) -> BackspaceAction:
        """解析退格动作"""
        return BackspaceAction(
            count=data.get('count', 1),
            char_delay=data.get('char_delay', 0.05)
        )
    
    @staticmethod
    def parse_delete(data: dict) -> DeleteAction:
        """解析删除动作"""
        return DeleteAction(
            count=data.get('count', 1),
            char_delay=data.get('char_delay', 0.05)
        )
    
    @staticmethod
    def parse_replace_text(data: dict) -> ReplaceTextAction:
        """解析替换动作"""
        return ReplaceTextAction(
            start=data['start'],
            end=data['end'],
            new_text=data.get('new_text', ''),
            duration=data.get('duration', 0.1)
        )
    
    @staticmethod
    def parse_move_cursor(data: dict) -> MoveCursorAction:
        """解析光标移动动作"""
        return MoveCursorAction(
            position=data.get('position'),
            offset=data.get('offset'),
            clear_selection=data.get('clear_selection', True),
            duration=data.get('duration', 0.02)
        )
    
    @staticmethod
    def parse_set_selection(data: dict) -> SetSelectionAction:
        """解析设置选区动作"""
        return SetSelectionAction(
            start=data['start'],
            end=data['end'],
            duration=data.get('duration', 0.05)
        )
    
    @staticmethod
    def parse_select_range(data: dict) -> SelectRangeAction:
        """解析范围选择动作"""
        return SelectRangeAction(
            start=data['start'],
            length=data['length'],
            duration=data.get('duration', 0.05)
        )
    
    @staticmethod
    def parse_clear_selection(data: dict) -> ClearSelectionAction:
        """解析清除选区动作"""
        return ClearSelectionAction(
            duration=data.get('duration', 0.01)
        )
    
    @staticmethod
    def parse_delete_selection(data: dict) -> DeleteSelectionAction:
        """解析删除选区动作"""
        return DeleteSelectionAction(
            duration=data.get('duration', 0.05)
        )
    
    @staticmethod
    def parse_set_style(data: dict) -> SetStyleAction:
        """解析设置样式动作"""
        style_name = data.get('style', 'normal').upper()
        style = TextStyle[style_name]
        return SetStyleAction(
            style=style,
            duration=data.get('duration', 0.01)
        )
    
    @staticmethod
    def parse_pause(data: dict) -> PauseAction:
        """解析停顿动作"""
        return PauseAction(duration=data.get('duration', 1.0))
    
    @classmethod
    def parse_composite(cls, data: dict) -> CompositeAction:
        """解析组合动作"""
        sub_actions = cls.parse_actions(data.get('actions', []))
        return CompositeAction(actions=sub_actions)


class ScriptBuilder:
    """脚本构建器（用于生成脚本）"""
    
    def __init__(self):
        self.actions = []
    
    def type(self, text: str, wpm: int = 60) -> 'ScriptBuilder':
        """添加打字动作"""
        self.actions.append({
            'type': 'type',
            'text': text,
            'wpm': wpm
        })
        return self
    
    def insert(self, text: str) -> 'ScriptBuilder':
        """添加插入动作"""
        self.actions.append({
            'type': 'insert',
            'text': text
        })
        return self
    
    def pause(self, duration: float) -> 'ScriptBuilder':
        """添加停顿"""
        self.actions.append({
            'type': 'pause',
            'duration': duration
        })
        return self
    
    def backspace(self, count: int = 1) -> 'ScriptBuilder':
        """添加退格"""
        self.actions.append({
            'type': 'backspace',
            'count': count
        })
        return self
    
    def select(self, start: int, end: int) -> 'ScriptBuilder':
        """添加选区"""
        self.actions.append({
            'type': 'select',
            'start': start,
            'end': end
        })
        return self
    
    def delete_selection(self) -> 'ScriptBuilder':
        """删除选区"""
        self.actions.append({
            'type': 'delete_selection'
        })
        return self
    
    def style(self, style: str) -> 'ScriptBuilder':
        """设置样式"""
        self.actions.append({
            'type': 'style',
            'style': style
        })
        return self
    
    def build(self) -> dict:
        """构建脚本字典"""
        return {'actions': self.actions}
    
    def to_json(self, indent: int = 2) -> str:
        """导出为 JSON"""
        return json.dumps(self.build(), indent=indent, ensure_ascii=False)
    
    def save(self, filepath: Union[str, Path]) -> None:
        """保存到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.build(), f, indent=2, ensure_ascii=False)


# ==================== 预设脚本模板 ====================

DEMO_SCRIPTS = {
    'hello_world': {
        'actions': [
            {'type': 'type', 'text': 'Hello, World!', 'wpm': 40},
            {'type': 'pause', 'duration': 0.5},
            {'type': 'backspace', 'count': 6},
            {'type': 'type', 'text': 'Python!', 'wpm': 40}
        ]
    },
    
    'code_editing': {
        'actions': [
            {'type': 'type', 'text': 'def hello():', 'wpm': 60},
            {'type': 'pause', 'duration': 0.3},
            {'type': 'type', 'text': '\n    print("Hello")', 'wpm': 60},
            {'type': 'pause', 'duration': 0.5},
            {'type': 'select', 'start': 20, 'end': 25},
            {'type': 'pause', 'duration': 0.2},
            {'type': 'type', 'text': 'World', 'wpm': 60}
        ]
    },
    
    'emoji_demo': {
        'actions': [
            {'type': 'type', 'text': 'I love coding ', 'wpm': 50},
            {'type': 'insert', 'text': '💻'},
            {'type': 'pause', 'duration': 0.3},
            {'type': 'insert', 'text': '🚀'},
            {'type': 'pause', 'duration': 0.3},
            {'type': 'insert', 'text': '✨'}
        ]
    }
}


def load_demo_script(name: str) -> list[Action]:
    """
    加载预设演示脚本
    
    Args:
        name: 脚本名称 ('hello_world', 'code_editing', 'emoji_demo')
    
    Returns:
        动作列表
    """
    if name not in DEMO_SCRIPTS:
        raise ValueError(f"Unknown demo script: {name}. Available: {list(DEMO_SCRIPTS.keys())}")
    
    return ScriptParser.parse(DEMO_SCRIPTS[name])
