# Typing Replay Engine - 高级教程

本教程介绍高级特性和最佳实践，帮助您充分发挥 Typing Replay Engine 的潜力。

## 📋 目录

1. [高级脚本技巧](#高级脚本技巧)
2. [性能优化](#性能优化)
3. [GUI 扩展](#gui-扩展)
4. [编程集成](#编程集成)
5. [最佳实践](#最佳实践)

---

## 高级脚本技巧

### 1. 复杂选区操作

**场景**: 多次选择和编辑

```json
{
  "actions": [
    {"type": "type", "text": "function hello(name, age, city) {", "wpm": 75},
    {"type": "pause", "duration": 0.5},
    
    {"type": "select", "start": 15, "end": 19},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "person", "wpm": 70},
    
    {"type": "pause", "duration": 0.5},
    {"type": "move_cursor", "position": 34},
    {"type": "type", "text": "\n  console.log(`Hello ${person}!`);", "wpm": 70},
    {"type": "type", "text": "\n}", "wpm": 75}
  ]
}
```

**要点**:
- 精确计算光标位置
- 合理安排选区范围
- 注意文本长度变化

---

### 2. 条件式编辑流程

**场景**: 模拟思考和决策

```json
{
  "actions": [
    {"type": "type", "text": "const result = calculateTotal(", "wpm": 75},
    {"type": "pause", "duration": 1.0},
    
    {"type": "type", "text": "items", "wpm": 70},
    {"type": "pause", "duration": 0.8},
    {"type": "backspace", "count": 5},
    {"type": "pause", "duration": 0.5},
    
    {"type": "type", "text": "data.items", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": ");", "wpm": 75}
  ]
}
```

**技巧**:
- 长停顿表示思考
- 删除重写显示决策
- 速度变化体现不确定性

---

### 3. 分层脚本组织

**创建可维护的脚本**:

```python
# 使用 ScriptBuilder 构建复杂脚本
from script_parser import ScriptBuilder

def create_function_demo():
    """创建函数演示脚本"""
    builder = ScriptBuilder()
    
    # 函数定义
    builder.type("def process_data(items):", wpm=75) \
           .pause(0.3)
    
    # 文档字符串
    builder.type('\n    """处理数据列表"""', wpm=70) \
           .pause(0.4)
    
    # 函数体
    builder.type("\n    result = []", wpm=75) \
           .pause(0.3) \
           .type("\n    for item in items:", wpm=75) \
           .pause(0.3) \
           .type("\n        result.append(item * 2)", wpm=70) \
           .pause(0.3) \
           .type("\n    return result", wpm=75)
    
    return builder.build()

# 保存为文件
builder = ScriptBuilder()
# ... 构建脚本 ...
builder.save('function_demo.json')
```

---

### 4. 动态参数生成

**根据内容自动调整参数**:

```python
def create_adaptive_script(text, base_wpm=60):
    """根据文本长度自动调整速度"""
    builder = ScriptBuilder()
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        # 短行快速打字
        wpm = base_wpm + 10 if len(line) < 30 else base_wpm
        
        builder.type(line, wpm=wpm)
        
        # 段落间增加停顿
        if i < len(lines) - 1:
            pause_time = 0.5 if line.endswith('.') else 0.3
            builder.pause(pause_time)
            builder.type('\n', wpm=80)
    
    return builder.build()
```

---

## 性能优化

### 1. 大文本处理

**问题**: 逐字打字大段文本太慢

**解决方案**: 混合使用 `type` 和 `insert`

```json
{
  "actions": [
    {"type": "type", "text": "# 标题\n\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    
    {"type": "insert", "text": "这里是一大段已经准备好的文本内容...\n(省略几百字)\n"},
    
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "重点内容需要逐字显示。", "wpm": 50}
  ]
}
```

**原则**:
- 不重要的文本用 `insert`
- 关键演示内容用 `type`
- 节省时间，突出重点

---

### 2. 减少动作数量

**低效示例**:
```json
{
  "actions": [
    {"type": "type", "text": "a", "wpm": 60},
    {"type": "type", "text": "b", "wpm": 60},
    {"type": "type", "text": "c", "wpm": 60}
  ]
}
```

**优化后**:
```json
{
  "actions": [
    {"type": "type", "text": "abc", "wpm": 60}
  ]
}
```

**收益**: 减少解析和执行开销

---

### 3. 预计算时长

```python
from script_parser import ScriptParser
from scheduler import PlaybackScheduler

# 加载脚本
actions = ScriptParser.parse('demo_script.json')

# 计算总时长
scheduler = PlaybackScheduler()
scheduler.add_actions(actions)
total_duration = scheduler.get_total_duration()

print(f"预计播放时长: {total_duration:.2f} 秒")
```

**用途**:
- 视频时长规划
- 进度条计算
- 资源分配

---

## GUI 扩展

### 1. 自定义主题

修改 `gui.py` 中的配色：

```python
self.colors = {
    'bg': '#1e1e1e',           # 深色背景
    'fg': '#d4d4d4',           # 浅色文字
    'primary': '#007acc',      # VS Code 蓝
    'success': '#4ec9b0',      # 青绿色
    'warning': '#dcdcaa',      # 黄色
    'danger': '#f48771',       # 红色
    'editor_bg': '#252526',    # 编辑器背景
    'editor_fg': '#d4d4d4',    # 编辑器文字
}
```

---

### 2. 添加快捷键

在 `__init__` 方法中绑定快捷键：

```python
def __init__(self, root):
    # ... 其他初始化代码 ...
    
    # 绑定快捷键
    self.root.bind('<Control-o>', lambda e: self.load_script_file())
    self.root.bind('<Control-s>', lambda e: self.save_script_file())
    self.root.bind('<space>', lambda e: self.play_script())
    self.root.bind('<F5>', lambda e: self.validate_script())
```

---

### 3. 导出功能

添加导出到视频或 GIF 的功能：

```python
def export_to_frames(self):
    """导出为帧序列"""
    try:
        script_text = self.script_editor.get("1.0", tk.END)
        script = json.loads(script_text)
        actions = ScriptParser.parse(script)
        
        scheduler = PlaybackScheduler()
        scheduler.add_actions(actions)
        
        frames = []
        
        def capture_frame(state, timestamp):
            frames.append({
                'time': timestamp,
                'text': state.text,
                'cursor': state.cursor_pos
            })
        
        # 以 30 FPS 导出
        scheduler.play_with_frame_callback(capture_frame, fps=30)
        
        # 保存帧数据
        import json
        with open('frames.json', 'w') as f:
            json.dump(frames, f, indent=2)
        
        messagebox.showinfo("成功", f"已导出 {len(frames)} 帧")
        
    except Exception as e:
        messagebox.showerror("错误", f"导出失败:\n{str(e)}")
```

---

## 编程集成

### 1. 嵌入到应用

```python
from typing_replay import PlaybackScheduler, type_text, pause

class MyApp:
    def __init__(self):
        self.scheduler = PlaybackScheduler()
    
    def show_tutorial(self):
        """显示教程动画"""
        self.scheduler.clear_actions()
        
        self.scheduler.add_actions([
            type_text("欢迎使用本应用！", wpm=60),
            pause(1.0),
            type_text("\n让我们开始吧...", wpm=55)
        ])
        
        # 设置回调更新 UI
        self.scheduler.on_state_changed(self.update_tutorial_display)
        
        # 播放
        self.scheduler.play(real_time=True)
    
    def update_tutorial_display(self, state):
        """更新教程显示"""
        self.tutorial_label.config(text=state.text)
```

---

### 2. 批量生成脚本

```python
def generate_code_demos(functions):
    """为多个函数生成演示脚本"""
    scripts = {}
    
    for func_name, func_code in functions.items():
        builder = ScriptBuilder()
        
        # 添加注释
        builder.type(f"# {func_name} 演示\n\n", wpm=70)
        builder.pause(0.5)
        
        # 添加代码
        lines = func_code.split('\n')
        for line in lines:
            builder.type(line + '\n', wpm=75)
            builder.pause(0.3)
        
        scripts[func_name] = builder.build()
    
    return scripts

# 使用
functions = {
    'fibonacci': 'def fibonacci(n):\n    ...',
    'factorial': 'def factorial(n):\n    ...',
}

demos = generate_code_demos(functions)
```

---

### 3. 测试自动化

```python
import unittest
from typing_replay import PlaybackScheduler, type_text

class TestScriptGeneration(unittest.TestCase):
    def test_basic_typing(self):
        """测试基础打字"""
        scheduler = PlaybackScheduler()
        scheduler.add_action(type_text("Hello", wpm=60))
        scheduler.play()
        
        self.assertEqual(scheduler.buffer.text, "Hello")
    
    def test_script_duration(self):
        """测试时长计算"""
        scheduler = PlaybackScheduler()
        scheduler.add_actions([
            type_text("Test", wpm=60),
            pause(1.0)
        ])
        
        duration = scheduler.get_total_duration()
        self.assertGreater(duration, 1.0)

if __name__ == '__main__':
    unittest.main()
```

---

## 最佳实践

### 1. 脚本设计原则

#### ✅ 好的实践

```json
{
  "actions": [
    {"type": "type", "text": "import numpy as np", "wpm": 75},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\nimport pandas as pd", "wpm": 75},
    {"type": "pause", "duration": 0.5},
    
    {"type": "type", "text": "\n\n# 加载数据", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\ndata = pd.read_csv('file.csv')", "wpm": 70}
  ]
}
```

**优点**:
- 速度适中
- 停顿合理
- 结构清晰

#### ❌ 避免的做法

```json
{
  "actions": [
    {"type": "type", "text": "import numpy as np\nimport pandas as pd\n\n# 加载数据\ndata = pd.read_csv('file.csv')", "wpm": 100}
  ]
}
```

**问题**:
- 速度太快
- 无停顿
- 难以跟随

---

### 2. 速度选择指南

| 内容类型 | 推荐 WPM | 说明 |
|---------|---------|------|
| 普通文本 | 50-60 | 舒适阅读速度 |
| 代码 | 70-80 | 稍快，体现熟练 |
| 命令 | 75-85 | 快速输入 |
| 创意写作 | 40-50 | 慢速，体现思考 |
| 修正错误 | 60-70 | 中速 |
| 注释 | 65-75 | 略快 |

---

### 3. 停顿时机

```python
# 停顿时长参考
PAUSE_SHORT = 0.2      # 逗号、分号
PAUSE_MEDIUM = 0.5     # 句号、行尾
PAUSE_LONG = 1.0       # 段落、思考
PAUSE_VERY_LONG = 2.0  # 重要转折
```

**示例**:
```json
{
  "actions": [
    {"type": "type", "text": "第一句话，", "wpm": 60},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "继续。", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    
    {"type": "type", "text": "\n\n新段落开始。", "wpm": 60},
    {"type": "pause", "duration": 1.0}
  ]
}
```

---

### 4. 错误处理

```python
from typing_replay import ScriptParser, PlaybackScheduler

def safe_play_script(script_file):
    """安全播放脚本"""
    try:
        # 加载脚本
        actions = ScriptParser.parse(script_file)
        
        # 验证动作数量
        if len(actions) == 0:
            raise ValueError("脚本为空")
        
        if len(actions) > 1000:
            print("警告: 动作数量过多，可能影响性能")
        
        # 创建调度器
        scheduler = PlaybackScheduler()
        scheduler.add_actions(actions)
        
        # 预计时长
        duration = scheduler.get_total_duration()
        print(f"预计播放时长: {duration:.2f} 秒")
        
        # 播放
        scheduler.play()
        
        return True
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {script_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"错误: JSON 格式错误 - {e}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False
```

---

### 5. 版本控制

**脚本文件命名**:
```
scripts/
  ├── demo_v1.json
  ├── demo_v2.json
  ├── tutorial_intro.json
  └── tutorial_advanced.json
```

**添加元数据**:
```json
{
  "meta": {
    "version": "1.0",
    "author": "Your Name",
    "description": "代码演示脚本",
    "created": "2024-01-15"
  },
  "actions": [
    ...
  ]
}
```

---

### 6. 性能监控

```python
from typing_replay import PlaybackScheduler, EventLogger

# 创建日志器
logger = EventLogger(verbose=True)

scheduler = PlaybackScheduler()
scheduler.on_action_executed(logger.log_event)

# 播放
scheduler.play()

# 查看统计
summary = logger.get_summary()
print(f"总动作数: {summary['total_events']}")
print(f"总时长: {summary['total_duration']:.2f}s")
print(f"动作分布: {summary['action_counts']}")
```

---

## 🎯 进阶项目

### 项目 1: 自动代码教程生成器

```python
def generate_tutorial_from_code(code, language='python'):
    """从代码自动生成教程脚本"""
    builder = ScriptBuilder()
    
    # 添加标题
    builder.type(f"# {language.title()} 教程\n\n", wpm=70)
    builder.pause(0.5)
    
    # 逐行分析
    lines = code.split('\n')
    for line in lines:
        # 识别注释
        if line.strip().startswith('#'):
            builder.pause(0.5)
            builder.type(line + '\n', wpm=55)
        # 识别函数定义
        elif 'def ' in line:
            builder.pause(0.3)
            builder.type(line + '\n', wpm=70)
        # 普通代码
        else:
            builder.type(line + '\n', wpm=75)
            builder.pause(0.2)
    
    return builder.build()
```

### 项目 2: 交互式文档系统

集成到 Jupyter Notebook 或 Streamlit，实现交互式教程。

### 项目 3: 视频字幕生成器

将脚本转换为 SRT 字幕文件，用于视频制作。

---

## 📚 延伸阅读

- [项目架构文档](ARCHITECTURE.md)
- [API 参考](README.md)
- [使用案例集](USE_CASES.md)

---

**持续学习，不断进步！** 🚀
