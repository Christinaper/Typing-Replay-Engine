# Typing Replay Engine

参数驱动的打字回放引擎，用于模拟真实的人类打字过程。

## 特性

- ✅ **模块化设计**: 清晰的架构，易于扩展和测试
- ✅ **丰富的动作集**: 支持打字、删除、选区、光标移动、样式切换等
- ✅ **时间控制**: 支持实时播放、倍速播放、帧率导出
- ✅ **脚本化**: 支持 JSON/Python dict 配置，可编程控制
- ✅ **交互模式**: 支持步进调试、暂停/继续
- ✅ **可观测性**: 提供回调、事件日志、状态快照
- ✅ **Unicode 支持**: 完美处理 Emoji 和多语言文本

## 快速开始

### 基础使用

```python
from typing_replay import create_replay, type_text, pause

# 创建回放调度器
scheduler = create_replay([
    type_text("Hello, World!", wpm=60),
    pause(0.5),
    type_text("\nWelcome!", wpm=50)
])

# 播放
scheduler.play()

# 获取最终文本
print(scheduler.buffer.text)
```

### 使用脚本配置

```python
from typing_replay import ScriptParser, PlaybackScheduler

# JSON 格式脚本
script = {
    "actions": [
        {"type": "type", "text": "Hello", "wpm": 60},
        {"type": "pause", "duration": 0.5},
        {"type": "backspace", "count": 5},
        {"type": "type", "text": "Hi!", "wpm": 50}
    ]
}

# 解析并播放
actions = ScriptParser.parse(script)
scheduler = PlaybackScheduler()
scheduler.add_actions(actions)
scheduler.play()
```

### 使用脚本构建器

```python
from typing_replay import ScriptBuilder

# 链式调用构建脚本
builder = ScriptBuilder()
builder.type("First line.", wpm=60) \
       .pause(0.5) \
       .type("\nSecond line.", wpm=70) \
       .backspace(5) \
       .type("paragraph!", wpm=65)

# 导出 JSON
print(builder.to_json())

# 或保存到文件
builder.save("script.json")
```

## 核心架构

### 1. Buffer (编辑状态模型)

```python
from typing_replay import TextBuffer

buffer = TextBuffer()
buffer.insert_text("Hello")
buffer.move_cursor(0)
buffer.set_selection(0, 5)
buffer.delete_selection()
```

**主要功能**:
- 文本缓冲区管理
- 光标位置控制
- 选区创建和删除
- 样式状态记录

### 2. Actions (动作抽象)

所有动作都继承自 `Action` 基类，实现 `execute()` 和 `get_duration()` 方法。

**内置动作**:
- `TypeTextAction` - 逐字符打字（带速度抖动）
- `InsertTextAction` - 即时插入
- `BackspaceAction` / `DeleteAction` - 删除字符
- `MoveCursorAction` - 光标移动
- `SetSelectionAction` - 创建选区
- `DeleteSelectionAction` - 删除选区
- `ReplaceTextAction` - 替换文本
- `SetStyleAction` - 设置样式
- `PauseAction` - 停顿
- `CompositeAction` - 组合动作

**便捷函数**:
```python
from typing_replay import type_text, pause, backspace, move_cursor, select

actions = [
    type_text("Hello", wpm=60),  # 每分钟 60 词
    pause(0.5),                   # 停顿 0.5 秒
    backspace(3),                 # 退格 3 次
    move_cursor(0),               # 移动到开头
    select(0, 5)                  # 选择前 5 个字符
]
```

### 3. Scheduler (调度器)

```python
from typing_replay import PlaybackScheduler

scheduler = PlaybackScheduler()

# 添加动作
scheduler.add_action(type_text("Hello"))
scheduler.add_actions([pause(0.5), type_text("World")])

# 设置回调
scheduler.on_action_executed(lambda event: print(event))
scheduler.on_state_changed(lambda state: print(state.text))

# 播放
events = scheduler.play(real_time=True, speed=2.0)  # 2倍速实时播放

# 获取统计
stats = scheduler.get_stats()
```

**InteractiveScheduler** 支持步进控制:
```python
from typing_replay import InteractiveScheduler

scheduler = InteractiveScheduler()
scheduler.add_actions(actions)

# 步进执行
while not scheduler.is_finished():
    event = scheduler.step()
    print(f"Progress: {scheduler.get_progress()*100:.1f}%")
    
# 回退
scheduler.step_back()
```

### 4. Script Parser (脚本解析)

支持的脚本格式:

```json
{
  "actions": [
    {
      "type": "type",
      "text": "Hello World",
      "wpm": 60
    },
    {
      "type": "pause",
      "duration": 0.5
    },
    {
      "type": "select",
      "start": 0,
      "end": 5
    },
    {
      "type": "backspace",
      "count": 3
    }
  ]
}
```

## 完整示例

### 示例 1: 编辑代码

```python
from typing_replay import PlaybackScheduler, type_text, pause, select

scheduler = PlaybackScheduler()

# 模拟编写函数
scheduler.add_actions([
    type_text("def calculate(", wpm=80),
    pause(0.2),
    type_text("a, b", wpm=70),
    type_text("):", wpm=80),
    pause(0.3),
    type_text("\n    return a + b", wpm=75),
    pause(0.5),
    # 修改函数名
    move_cursor(4),
    select(4, 13),  # 选择 "calculate"
    type_text("sum", wpm=80),
])

scheduler.play(real_time=True)
print(scheduler.buffer.text)
```

### 示例 2: 导出动画帧

```python
from typing_replay import PlaybackScheduler, type_text

scheduler = PlaybackScheduler()
scheduler.add_action(type_text("Animated text...", wpm=40))

frames = []

def capture_frame(state, timestamp):
    frames.append({
        'time': timestamp,
        'text': state.text,
        'cursor': state.cursor_pos
    })

# 以 30 FPS 导出
scheduler.play_with_frame_callback(capture_frame, fps=30)

# frames 现在包含所有帧数据，可用于生成视频
print(f"Captured {len(frames)} frames")
```

### 示例 3: 实时可视化

```python
from typing_replay import PlaybackScheduler, ConsoleRenderer, type_text, pause

scheduler = PlaybackScheduler()
renderer = ConsoleRenderer()

# 设置实时渲染回调
scheduler.on_state_changed(
    lambda state: renderer.render_state(state, clear_previous=True)
)

scheduler.add_actions([
    type_text("Watching in real-time...", wpm=50),
    pause(1.0),
    type_text("\nThis is cool!", wpm=60)
])

scheduler.play(real_time=True)
```

### 示例 4: 加载演示脚本

```python
from typing_replay import load_demo_script, PlaybackScheduler

# 加载内置演示脚本
actions = load_demo_script('code_editing')

scheduler = PlaybackScheduler()
scheduler.add_actions(actions)
scheduler.play()

print(scheduler.buffer.text)
```

## 运行示例和测试

### 运行所有示例

```bash
cd typing_replay
python examples.py
```

### 运行特定示例

```bash
python examples.py 1  # 运行示例 1
python examples.py 5  # 运行示例 5
```

### 运行测试

```bash
python test_engine.py
```

## 扩展性

### 自定义动作

```python
from typing_replay import Action, TextBuffer

class CustomAction(Action):
    def __init__(self, param):
        self.param = param
    
    def execute(self, buffer: TextBuffer) -> None:
        # 实现自定义逻辑
        buffer.insert_text(f"Custom: {self.param}")
    
    def get_duration(self) -> float:
        return 0.5

# 使用
scheduler.add_action(CustomAction("test"))
```

### 自定义回调

```python
def on_action(event):
    print(f"[{event.timestamp:.2f}s] {event.action}")
    print(f"Before: {event.state_before.text}")
    print(f"After: {event.state_after.text}")

scheduler.on_action_executed(on_action)
```

## API 参考

### TextBuffer

- `insert_text(text)` - 插入文本
- `delete_char(forward=False)` - 删除字符
- `move_cursor(position)` - 移动光标
- `set_selection(start, end)` - 设置选区
- `delete_selection()` - 删除选区
- `get_state(timestamp)` - 获取状态快照

### PlaybackScheduler

- `add_action(action)` - 添加动作
- `add_actions(actions)` - 批量添加
- `play(real_time=False, speed=1.0)` - 播放
- `on_action_executed(callback)` - 设置动作回调
- `on_state_changed(callback)` - 设置状态回调
- `get_stats()` - 获取统计信息

### ScriptParser

- `parse(script)` - 解析脚本
- `parse_actions(actions_data)` - 解析动作列表

### ScriptBuilder

- `type(text, wpm)` - 添加打字动作
- `pause(duration)` - 添加停顿
- `backspace(count)` - 添加退格
- `select(start, end)` - 添加选区
- `build()` - 构建脚本
- `to_json()` - 导出 JSON
- `save(filepath)` - 保存文件

## 文件结构

```
typing_replay/
├── __init__.py          # 主入口和便捷 API
├── buffer.py            # 编辑状态模型
├── actions.py           # 动作抽象
├── scheduler.py         # 调度器
├── script_parser.py     # 脚本解析器
├── console.py           # 控制台渲染工具
├── examples.py          # 示例代码
└── test_engine.py       # 单元测试
```

## 许可证

MIT License

## 作者

Created by Claude
