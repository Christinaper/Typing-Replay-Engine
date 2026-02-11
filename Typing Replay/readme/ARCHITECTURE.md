# Typing Replay Engine - 架构设计文档

## 1. 系统概览

### 1.1 设计目标

- **模块化**: 清晰的模块划分，低耦合高内聚
- **可扩展性**: 易于添加新的动作类型和功能
- **可测试性**: 完整的单元测试覆盖
- **可组合性**: 支持复杂的动作序列组合
- **时间控制**: 精确的时间模拟和回放控制

### 1.2 核心模块

```
typing_replay/
├── buffer.py          # 编辑状态模型
├── actions.py         # 动作抽象层
├── scheduler.py       # 调度与时间控制
├── script_parser.py   # 脚本解析与构建
├── console.py         # 可视化工具
└── __init__.py        # 公共 API
```

## 2. 核心架构

### 2.1 层次结构

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  (Examples, Tests, User Scripts)        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         API Layer                       │
│  (便捷函数, 脚本构建器)                  │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Scheduler Layer                 │
│  (时间控制, 事件管理)                    │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Action Layer                    │
│  (动作抽象, 具体动作实现)                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Buffer Layer                    │
│  (文本缓冲区, 光标, 选区)                │
└─────────────────────────────────────────┘
```

### 2.2 数据流

```
Script/Config
     ↓
  Parser
     ↓
  Actions[] → Scheduler → Events[]
                  ↓
              TextBuffer
                  ↓
            EditorState
                  ↓
         Callbacks/Rendering
```

## 3. 模块详解

### 3.1 Buffer Layer (buffer.py)

**职责**: 维护编辑器的核心状态

**核心类**:

1. **TextBuffer**
   - 管理文本内容
   - 光标位置跟踪
   - 选区管理
   - 样式状态记录

2. **Selection**
   - 表示文本选区
   - 自动处理 start/end 排序
   - 提供便捷的选区操作

3. **EditorState**
   - 不可变的状态快照
   - 用于历史记录和回放

**设计模式**:
- 命令模式: 所有操作通过方法调用
- 快照模式: 通过 `get_state()` 获取不可变快照

**关键方法**:
```python
# 文本操作
insert_text(text)
delete_char(forward=False)
replace_text(start, end, new_text)

# 光标操作
move_cursor(position)
move_cursor_relative(offset)

# 选区操作
set_selection(start, end)
delete_selection()

# 状态查询
get_state(timestamp) -> EditorState
```

### 3.2 Action Layer (actions.py)

**职责**: 定义所有可执行的编辑操作

**核心接口**:
```python
class Action(ABC):
    @abstractmethod
    def execute(self, buffer: TextBuffer) -> None:
        """执行动作"""
        pass
    
    @abstractmethod
    def get_duration(self) -> float:
        """获取持续时间"""
        pass
```

**动作分类**:

1. **文本编辑动作**
   - `TypeTextAction`: 模拟逐字符打字
   - `InsertTextAction`: 即时插入
   - `BackspaceAction`: 退格删除
   - `DeleteAction`: Delete 键删除
   - `ReplaceTextAction`: 替换指定范围

2. **导航动作**
   - `MoveCursorAction`: 光标移动
   - `SetSelectionAction`: 创建选区
   - `SelectRangeAction`: 范围选择

3. **控制动作**
   - `PauseAction`: 停顿
   - `SetStyleAction`: 样式切换
   - `CallbackAction`: 自定义回调

4. **组合动作**
   - `CompositeAction`: 组合多个子动作

**设计模式**:
- 策略模式: Action 作为可替换的策略
- 组合模式: CompositeAction 组合多个子动作

### 3.3 Scheduler Layer (scheduler.py)

**职责**: 管理动作序列的执行和时间控制

**核心类**:

1. **PlaybackScheduler**
   - 动作序列管理
   - 时间累积计算
   - 事件生成和回调
   - 支持实时/倍速播放

2. **InteractiveScheduler**
   - 继承自 PlaybackScheduler
   - 支持步进执行
   - 支持回退（通过重放）

**事件模型**:
```python
@dataclass
class PlaybackEvent:
    timestamp: float
    action: Action
    state_before: EditorState
    state_after: EditorState
```

**回调机制**:
```python
# 动作执行回调
on_action_executed(callback: Callable[[PlaybackEvent], None])

# 状态变化回调
on_state_changed(callback: Callable[[EditorState], None])
```

**播放模式**:

1. **批量播放**: `play(real_time=False)`
   - 立即执行所有动作
   - 返回完整事件列表

2. **实时播放**: `play(real_time=True, speed=1.0)`
   - 按动作持续时间延迟
   - 支持速度调整

3. **帧回放**: `play_with_frame_callback(callback, fps=30)`
   - 固定帧率采样
   - 适合生成动画

### 3.4 Script Parser Layer (script_parser.py)

**职责**: 解析和生成脚本

**核心类**:

1. **ScriptParser**
   - 支持 JSON 字符串
   - 支持 Python 字典
   - 支持文件路径
   - 动作类型映射

2. **ScriptBuilder**
   - 流式 API 构建脚本
   - 导出 JSON
   - 保存到文件

**脚本格式**:
```json
{
  "actions": [
    {
      "type": "type",
      "text": "Hello",
      "wpm": 60
    },
    {
      "type": "pause",
      "duration": 0.5
    }
  ]
}
```

**设计模式**:
- 工厂模式: 根据类型创建动作实例
- 构建器模式: ScriptBuilder 提供流式 API

### 3.5 Console Layer (console.py)

**职责**: 提供可视化和调试工具

**核心类**:

1. **ConsoleRenderer**
   - 实时渲染编辑器状态
   - 显示光标和选区
   - 支持清屏重绘

2. **EventLogger**
   - 记录所有事件
   - 生成统计摘要
   - 详细日志输出

3. **SimpleDisplay**
   - 简单的文本显示
   - 状态对比显示

## 4. 关键设计决策

### 4.1 为什么使用命令模式？

**优点**:
- 动作可序列化（保存/加载脚本）
- 易于撤销/重做（通过重放）
- 可组合、可测试
- 解耦动作定义和执行

**权衡**:
- 需要定义更多类
- 轻微的性能开销

### 4.2 时间模型

**设计**:
- 每个动作有 `get_duration()` 方法
- Scheduler 累积时间戳
- 支持多种播放模式

**优点**:
- 灵活的时间控制
- 精确的帧率导出
- 可预测的回放

### 4.3 状态快照 vs 事件溯源

**选择**: 混合方法
- 使用 EditorState 快照记录状态
- PlaybackEvent 包含前后状态
- 可选的事件溯源（通过重放）

**理由**:
- 快照简单直接
- 事件溯源支持撤销
- 混合提供最大灵活性

### 4.4 回调 vs 观察者模式

**选择**: 函数回调
- `on_action_executed(callback)`
- `on_state_changed(callback)`

**理由**:
- Python 风格的简洁 API
- 避免观察者模式的复杂性
- 易于使用和理解

## 5. 扩展点

### 5.1 添加新动作

```python
from typing_replay import Action, TextBuffer

class CustomAction(Action):
    def __init__(self, param):
        self.param = param
    
    def execute(self, buffer: TextBuffer) -> None:
        # 实现自定义逻辑
        pass
    
    def get_duration(self) -> float:
        return 0.5
```

### 5.2 自定义调度器

```python
from typing_replay import PlaybackScheduler

class CustomScheduler(PlaybackScheduler):
    def play(self, **kwargs):
        # 添加自定义播放逻辑
        return super().play(**kwargs)
```

### 5.3 扩展脚本解析

```python
from typing_replay import ScriptParser

class CustomParser(ScriptParser):
    ACTION_TYPES = {
        **ScriptParser.ACTION_TYPES,
        'custom': 'parse_custom'
    }
    
    @staticmethod
    def parse_custom(data):
        return CustomAction(data['param'])
```

## 6. 性能考虑

### 6.1 时间复杂度

- `insert_text`: O(n) - 字符串拼接
- `delete_char`: O(n) - 字符串切片
- `move_cursor`: O(1)
- `set_selection`: O(1)

### 6.2 空间复杂度

- TextBuffer: O(n) - 文本长度
- Events: O(m) - 动作数量
- 每个 EditorState: O(n) - 文本拷贝

### 6.3 优化建议

1. **大量文本**:
   - 使用 rope 数据结构替代字符串
   - 使用 gap buffer

2. **大量事件**:
   - 流式处理而非缓存所有事件
   - 按需生成快照

3. **实时性能**:
   - 预计算所有动作持续时间
   - 使用异步播放

## 7. 测试策略

### 7.1 单元测试

- 每个模块独立测试
- 覆盖边界情况
- 参数验证测试

### 7.2 集成测试

- 端到端工作流
- 脚本解析和执行
- 回调和事件系统

### 7.3 性能测试

- 大文本处理
- 长动作序列
- 内存使用监控

## 8. 未来改进方向

### 8.1 功能增强

- [ ] 多光标支持
- [ ] 折叠/展开支持
- [ ] 语法高亮集成
- [ ] 协作编辑模拟

### 8.2 性能优化

- [ ] Rope 数据结构
- [ ] 增量渲染
- [ ] 并发播放

### 8.3 工具集成

- [ ] GUI 编辑器
- [ ] 视频录制器
- [ ] Web 演示页面
- [ ] VS Code 插件

## 9. 总结

Typing Replay Engine 采用了清晰的分层架构和成熟的设计模式：

- **Buffer Layer**: 状态管理的核心
- **Action Layer**: 灵活的命令模式
- **Scheduler Layer**: 强大的时间控制
- **Script Layer**: 易用的配置接口

这种设计确保了系统的：
- ✅ 可扩展性 - 易于添加新功能
- ✅ 可测试性 - 完整的测试覆盖
- ✅ 可维护性 - 清晰的模块边界
- ✅ 易用性 - 简洁的 API 设计
