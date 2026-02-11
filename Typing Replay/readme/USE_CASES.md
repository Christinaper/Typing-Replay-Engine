# Typing Replay Engine - 使用案例

## 案例 1: 教程视频制作

### 场景
为 YouTube 编程教程创建逼真的打字动画。

### 实现
```python
from typing_replay import PlaybackScheduler, type_text, pause, backspace, select

scheduler = PlaybackScheduler()

# 模拟真实的编程过程，包括思考、修正
scheduler.add_actions([
    # 写函数签名
    type_text("def fibonacci(n):", wpm=70),
    pause(0.5),  # 思考
    
    # 写基本情况
    type_text("\n    if n <= 1:", wpm=65),
    type_text("\n        return n", wpm=65),
    pause(0.8),
    
    # 写递归情况（有拼写错误）
    type_text("\n    return fibbonacci(n-1) + fibonacci(n-2)", wpm=60),
    pause(1.0),  # 发现错误
    
    # 修正拼写错误
    select(67, 77),  # 选择 "fibbonacci"
    pause(0.3),
    type_text("fibonacci", wpm=70),
    pause(0.5),
])

# 以 30 FPS 导出用于视频编辑
frames = []
scheduler.play_with_frame_callback(
    lambda state, t: frames.append({'t': t, 'text': state.text}),
    fps=30
)

# frames 可用于生成视频叠加层
```

### 使用
- Final Cut Pro / Premiere Pro: 导入帧序列
- After Effects: 使用表达式驱动文本
- 自定义录屏工具: 逐帧渲染

---

## 案例 2: 产品演示

### 场景
SaaS 产品的功能演示，展示实时协作编辑。

### 实现
```python
from typing_replay import PlaybackScheduler, type_text, pause, InsertTextAction

scheduler = PlaybackScheduler()

# 用户 A 打字
scheduler.add_actions([
    type_text("Product Requirements:\n", wpm=60),
    pause(0.5),
    type_text("1. User authentication", wpm=55),
])

# 模拟用户 B 同时添加内容（使用回调）
def user_b_action(buffer):
    buffer.move_cursor(buffer.length)
    buffer.insert_text("\n2. Dashboard analytics")

from typing_replay import CallbackAction
scheduler.add_action(CallbackAction(user_b_action, name="User B types"))

scheduler.add_actions([
    pause(0.5),
    type_text("\n3. Real-time collaboration 🚀", wpm=60),
])

# 实时播放用于现场演示
scheduler.play(real_time=True)
```

---

## 案例 3: 代码审查培训

### 场景
教新员工如何审查代码，演示思考过程。

### 实现
```python
from typing_replay import PlaybackScheduler, type_text, pause, select, InsertTextAction

scheduler = PlaybackScheduler()

# 原始代码
original_code = """def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result"""

# 添加评论和建议
scheduler.add_actions([
    InsertTextAction(original_code),
    pause(2.0),  # "阅读"代码
    
    # 添加第一条评论
    type_text("\n\n# Review: ", wpm=60),
    pause(0.5),
    type_text("Consider using list comprehension", wpm=55),
    pause(1.0),
    
    # 展示改进版本
    type_text("\n# Improved version:", wpm=60),
    pause(0.3),
    type_text("\ndef process_data(data):", wpm=70),
    type_text("\n    return [item * 2 for item in data]", wpm=65),
    pause(1.5),
    
    # 添加性能说明
    type_text("\n# More Pythonic and faster ✨", wpm=60),
])

scheduler.play(real_time=True, speed=1.5)
```

---

## 案例 4: 交互式文档

### 场景
创建可交互的 Markdown 文档，逐步展示内容。

### 实现
```python
from typing_replay import InteractiveScheduler, type_text, pause
from IPython.display import display, Markdown, clear_output

scheduler = InteractiveScheduler()

sections = [
    ("# Introduction\n", 60),
    ("This is an interactive document.\n\n", 55),
    ("## Key Points\n", 60),
    ("- Point 1: Modularity\n", 55),
    ("- Point 2: Extensibility\n", 55),
    ("- Point 3: Testability\n", 55),
]

for text, wpm in sections:
    scheduler.add_action(type_text(text, wpm=wpm))
    scheduler.add_action(pause(0.5))

# Jupyter Notebook 中逐步显示
import time
while not scheduler.is_finished():
    scheduler.step()
    clear_output(wait=True)
    display(Markdown(scheduler.buffer.text))
    time.sleep(0.5)
```

---

## 案例 5: A/B 测试脚本

### 场景
测试不同的打字速度对用户体验的影响。

### 实现
```python
from typing_replay import PlaybackScheduler, type_text

def create_demo(wpm_profile):
    """根据不同速度配置创建演示"""
    scheduler = PlaybackScheduler()
    
    scheduler.add_actions([
        type_text("Welcome to our app!", wpm=wpm_profile['welcome']),
        pause(0.5),
        type_text("\nClick here to get started.", wpm=wpm_profile['cta']),
    ])
    
    return scheduler

# A 组: 快速打字
demo_a = create_demo({'welcome': 80, 'cta': 70})

# B 组: 慢速打字（更人性化）
demo_b = create_demo({'welcome': 50, 'cta': 45})

# 收集指标
import time

start = time.time()
demo_a.play(real_time=True)
duration_a = time.time() - start

start = time.time()
demo_b.play(real_time=True)
duration_b = time.time() - start

print(f"Demo A: {duration_a:.2f}s")
print(f"Demo B: {duration_b:.2f}s")
```

---

## 案例 6: 自动化测试

### 场景
测试富文本编辑器的边界情况。

### 实现
```python
from typing_replay import PlaybackScheduler, type_text, backspace, select, delete_selection

def test_editor_robustness():
    """测试编辑器是否正确处理各种操作"""
    test_cases = [
        # 测试 1: 空文档删除
        [backspace(5)],
        
        # 测试 2: 选区边界
        [
            type_text("Hello", wpm=100),
            select(0, 10),  # 超出范围
            delete_selection(),
        ],
        
        # 测试 3: Unicode 处理
        [
            type_text("Hello 世界 🌍", wpm=100),
            backspace(3),
        ],
    ]
    
    results = []
    for i, actions in enumerate(test_cases):
        scheduler = PlaybackScheduler()
        scheduler.add_actions(actions)
        
        try:
            scheduler.play()
            results.append(f"Test {i+1}: PASS")
        except Exception as e:
            results.append(f"Test {i+1}: FAIL - {e}")
    
    return results

# 运行测试
results = test_editor_robustness()
for result in results:
    print(result)
```

---

## 案例 7: 创意写作工具

### 场景
小说写作过程的可视化，展示思路演变。

### 实现
```python
from typing_replay import PlaybackScheduler, type_text, pause, backspace, select

scheduler = PlaybackScheduler()

# 模拟创作过程
scheduler.add_actions([
    # 第一版
    type_text("The dark night was silent.", wpm=45),
    pause(2.0),  # 停顿思考
    
    # 不满意，重写
    select(4, 8),  # 选择 "dark"
    type_text("moonless", wpm=40),
    pause(1.5),
    
    # 继续扩展
    type_text(" Stars twinkled overhead", wpm=42),
    pause(1.0),
    
    # 添加细节
    backspace(8),  # 删除 "overhead"
    type_text("in the velvet sky", wpm=45),
    pause(0.5),
    type_text(", indifferent to the drama below.", wpm=50),
])

# 导出为创作时间线
events = scheduler.play()

print("Writing Timeline:")
for event in events:
    if hasattr(event.action, 'text'):
        print(f"[{event.timestamp:.1f}s] Added: {event.action.text}")
    elif event.action.__class__.__name__ == 'BackspaceAction':
        print(f"[{event.timestamp:.1f}s] Deleted {event.action.count} chars")
```

---

## 案例 8: 编程竞赛回放

### 场景
回放编程竞赛选手的解题过程。

### 实现
```python
from typing_replay import ScriptParser, PlaybackScheduler

# 从竞赛录像中提取的动作序列
competition_script = {
    "actions": [
        {"type": "type", "text": "# Problem: Two Sum\n", "wpm": 90},
        {"type": "pause", "duration": 0.3},
        
        {"type": "type", "text": "def two_sum(nums, target):\n", "wpm": 85},
        {"type": "type", "text": "    seen = {}\n", "wpm": 80},
        {"type": "type", "text": "    for i, num in enumerate(nums):\n", "wpm": 75},
        {"type": "pause", "duration": 0.5},
        
        {"type": "type", "text": "        complement = target - num\n", "wpm": 70},
        {"type": "type", "text": "        if complement in seen:\n", "wpm": 75},
        {"type": "type", "text": "            return [seen[complement], i]\n", "wpm": 70},
        {"type": "type", "text": "        seen[num] = i\n", "wpm": 75},
        {"type": "pause", "duration": 1.0},
        
        # 测试
        {"type": "type", "text": "\n# Test\n", "wpm": 80},
        {"type": "type", "text": "print(two_sum([2,7,11,15], 9))", "wpm": 75},
    ]
}

actions = ScriptParser.parse(competition_script)
scheduler = PlaybackScheduler()
scheduler.add_actions(actions)

# 记录关键节点
milestones = []

def track_milestone(event):
    if "def two_sum" in event.state_after.text and len(milestones) == 0:
        milestones.append(("Function defined", event.timestamp))
    elif "complement in seen" in event.state_after.text and len(milestones) == 1:
        milestones.append(("Logic implemented", event.timestamp))
    elif "print(two_sum" in event.state_after.text:
        milestones.append(("Testing added", event.timestamp))

scheduler.on_action_executed(track_milestone)
scheduler.play()

print("\nKey Milestones:")
for milestone, timestamp in milestones:
    print(f"  {timestamp:.1f}s: {milestone}")
```

---

## 案例 9: 文档版本演变

### 场景
展示文档从草稿到最终版本的演变过程。

### 实现
```python
from typing_replay import PlaybackScheduler, type_text, pause, select

scheduler = PlaybackScheduler()

# V1: 草稿
scheduler.add_actions([
    type_text("# Project Proposal\n\n", wpm=60),
    type_text("We should build a new feature.\n", wpm=55),
    pause(2.0),
])

# V2: 添加细节
scheduler.add_actions([
    select(0, scheduler.buffer.length),
    type_text("# New Feature Proposal\n\n", wpm=60),
    type_text("## Problem\n", wpm=60),
    type_text("Users need better analytics.\n\n", wpm=55),
    type_text("## Solution\n", wpm=60),
    type_text("Build a dashboard with real-time metrics.\n", wpm=55),
    pause(3.0),
])

# V3: 润色
# ... 继续添加改进

# 创建版本标记
versions = []

def mark_version(event):
    if event.action.__class__.__name__ == 'PauseAction':
        versions.append({
            'timestamp': event.timestamp,
            'content': event.state_after.text
        })

scheduler.on_action_executed(mark_version)
scheduler.play()

# 导出版本历史
for i, version in enumerate(versions, 1):
    print(f"\n=== Version {i} @ {version['timestamp']:.1f}s ===")
    print(version['content'])
```

---

## 案例 10: 可访问性测试

### 场景
测试屏幕阅读器如何处理动态文本更新。

### 实现
```python
from typing_replay import PlaybackScheduler, type_text, pause

scheduler = PlaybackScheduler()

# 模拟聊天消息
messages = [
    "Alice: Hello!",
    "Bob: Hi Alice!",
    "Alice: How are you?",
    "Bob: Great, thanks!",
]

for msg in messages:
    scheduler.add_actions([
        type_text(msg + "\n", wpm=70),
        pause(1.0),  # 给屏幕阅读器时间
    ])

# 监控状态变化，用于辅助功能测试
aria_updates = []

def track_aria(state):
    # 模拟 ARIA live region 更新
    aria_updates.append({
        'timestamp': state.timestamp,
        'aria_label': f"{len(state.text.split(chr(10)))} messages",
        'text': state.text
    })

scheduler.on_state_changed(track_aria)
scheduler.play()

# 分析可访问性
print("Accessibility Timeline:")
for update in aria_updates[-5:]:  # 最后 5 个更新
    print(f"  {update['timestamp']:.1f}s: {update['aria_label']}")
```

---

## 最佳实践

### 1. 真实感打字
```python
# ✅ 好: 变化的速度和停顿
scheduler.add_actions([
    type_text("import numpy as np", wpm=75),  # 熟悉的代码
    pause(0.3),
    type_text("\nimport matplotlib", wpm=60),  # 稍慢，思考
    backspace(10),  # 拼写错误
    type_text("matplotlib.pyplot as plt", wpm=65),
])

# ❌ 差: 机械式，无变化
scheduler.add_actions([
    type_text("import numpy as np", wpm=60),
    type_text("\nimport matplotlib.pyplot as plt", wpm=60),
])
```

### 2. 性能优化
```python
# ✅ 好: 大段文本用 InsertTextAction
from typing_replay import InsertTextAction

long_text = """..."""  # 1000+ 字符
scheduler.add_action(InsertTextAction(long_text))

# ❌ 差: 大段文本逐字符打字
scheduler.add_action(type_text(long_text, wpm=60))  # 太慢
```

### 3. 模块化
```python
# ✅ 好: 可复用的动作序列
def create_header(text, wpm=60):
    return [
        type_text(f"# {text}\n\n", wpm=wpm),
        pause(0.3),
    ]

scheduler.add_actions(create_header("Introduction"))
scheduler.add_actions(create_header("Methods"))
```

---

这些案例展示了 Typing Replay Engine 的灵活性和实用性，涵盖从视频制作到自动化测试的各种场景。
