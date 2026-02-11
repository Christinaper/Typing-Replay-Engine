"""
快速入门指南
Typing Replay Engine Quick Start Guide
"""

# ============================================================
# 方式 1: 使用 Python 代码直接创建动作
# ============================================================

from typing_replay import (
    PlaybackScheduler, type_text, pause, backspace,
    move_cursor, select, delete_selection
)

# 创建调度器
scheduler = PlaybackScheduler()

# 添加动作序列
scheduler.add_actions([
    type_text("Hello, World!", wpm=60),  # 60 词/分钟
    pause(0.5),                           # 停顿 0.5 秒
    backspace(6),                         # 删除 "World!"
    type_text("Python!", wpm=50),         # 替换文本
])

# 播放
events = scheduler.play()

# 获取最终文本
print("Final text:", scheduler.buffer.text)
# 输出: Hello, Python!


# ============================================================
# 方式 2: 使用脚本构建器
# ============================================================

from typing_replay import ScriptBuilder, ScriptParser, PlaybackScheduler

# 构建脚本
builder = ScriptBuilder()
builder.type("First paragraph.", wpm=60) \
       .pause(0.5) \
       .type("\nSecond paragraph.", wpm=70) \
       .pause(0.3) \
       .backspace(10) \
       .type("sentence!", wpm=65)

# 方法 A: 直接使用
actions = ScriptParser.parse(builder.build())
scheduler = PlaybackScheduler()
scheduler.add_actions(actions)
scheduler.play()

# 方法 B: 保存为文件
builder.save("my_script.json")


# ============================================================
# 方式 3: 从 JSON 文件加载
# ============================================================

from typing_replay import ScriptParser, PlaybackScheduler

# 从文件加载
actions = ScriptParser.parse("demo_script.json")

scheduler = PlaybackScheduler()
scheduler.add_actions(actions)
scheduler.play()


# ============================================================
# 方式 4: 使用便捷 API
# ============================================================

from typing_replay import quick_play, create_replay

# 快速播放
text = quick_play({
    "actions": [
        {"type": "type", "text": "Quick demo", "wpm": 60},
        {"type": "pause", "duration": 0.5}
    ]
})

# 或使用 create_replay
scheduler = create_replay([
    type_text("Another example", wpm=60)
])
scheduler.play()


# ============================================================
# 高级特性 1: 实时播放
# ============================================================

from typing_replay import PlaybackScheduler, type_text, pause

scheduler = PlaybackScheduler()
scheduler.add_actions([
    type_text("Real-time typing...", wpm=60),
    pause(1.0)
])

# 实时播放（按实际时间延迟）
scheduler.play(real_time=True)

# 2倍速实时播放
scheduler.play(real_time=True, speed=2.0)


# ============================================================
# 高级特性 2: 回调和状态监控
# ============================================================

from typing_replay import PlaybackScheduler, EventLogger, type_text

scheduler = PlaybackScheduler()

# 方法 A: 使用事件日志器
logger = EventLogger(verbose=True)
scheduler.on_action_executed(logger.log_event)

# 方法 B: 自定义回调
def on_state_change(state):
    print(f"[{state.timestamp:.2f}s] Text: {state.text}")

scheduler.on_state_changed(on_state_change)

scheduler.add_action(type_text("Monitored typing", wpm=60))
scheduler.play()

# 打印统计摘要
logger.print_summary()


# ============================================================
# 高级特性 3: 交互式步进
# ============================================================

from typing_replay import InteractiveScheduler, type_text

scheduler = InteractiveScheduler()
scheduler.add_actions([
    type_text("Step ", wpm=60),
    type_text("by ", wpm=60),
    type_text("step", wpm=60)
])

# 逐步执行
while not scheduler.is_finished():
    event = scheduler.step()
    print(f"Current text: {scheduler.buffer.text}")
    print(f"Progress: {scheduler.get_progress()*100:.1f}%")

# 回退一步
scheduler.step_back()


# ============================================================
# 高级特性 4: 帧导出（用于动画）
# ============================================================

from typing_replay import PlaybackScheduler, type_text

scheduler = PlaybackScheduler()
scheduler.add_action(type_text("Animated text", wpm=40))

frames = []

def capture_frame(state, timestamp):
    frames.append({
        'time': timestamp,
        'text': state.text,
        'cursor': state.cursor_pos
    })

# 以 30 FPS 导出帧
scheduler.play_with_frame_callback(capture_frame, fps=30)

print(f"Captured {len(frames)} frames")
# 现在可以用 frames 数据生成视频或 GIF


# ============================================================
# 高级特性 5: 控制台实时渲染
# ============================================================

from typing_replay import PlaybackScheduler, ConsoleRenderer, type_text

scheduler = PlaybackScheduler()
renderer = ConsoleRenderer(show_cursor=True, show_selection=True)

# 设置实时渲染
scheduler.on_state_changed(
    lambda state: renderer.render_state(state, clear_previous=True)
)

scheduler.add_actions([
    type_text("Watch this text appear...", wpm=50),
    pause(1.0)
])

scheduler.play(real_time=True)


# ============================================================
# 完整示例: 模拟代码编辑
# ============================================================

from typing_replay import PlaybackScheduler, type_text, pause, select, move_cursor

scheduler = PlaybackScheduler()

# 模拟编写并修改代码
scheduler.add_actions([
    # 编写初始代码
    type_text("def calculate_sum(a, b):", wpm=80),
    pause(0.3),
    type_text("\n    return a + b", wpm=75),
    pause(0.5),
    
    # 修改函数名
    move_cursor(4),                    # 移动到 "calculate_sum" 开始
    select(4, 17),                     # 选择 "calculate_sum"
    type_text("multiply", wpm=80),     # 替换为 "multiply"
    
    # 修改操作符
    move_cursor(-1),                   # 移动到 "+"
    select(32, 35),                    # 选择 " + "
    type_text(" * ", wpm=60),          # 替换为 " * "
])

# 播放并查看结果
scheduler.play()
print("\nFinal code:")
print(scheduler.buffer.text)


# ============================================================
# 统计信息
# ============================================================

# 获取详细统计
stats = scheduler.get_stats()
print(f"\nTotal actions: {stats['total_actions']}")
print(f"Total duration: {stats['total_duration']:.2f}s")
print(f"Final text length: {stats['final_text_length']} chars")
print(f"Action breakdown: {stats['action_types']}")


# ============================================================
# 提示和技巧
# ============================================================

"""
1. 速度控制:
   - wpm (每分钟单词数): 通常 40-80 适合演示
   - delay_variance: 控制打字速度的自然波动

2. 停顿使用:
   - 0.2-0.5s: 短暂思考
   - 0.5-1.0s: 中等停顿
   - 1.0-2.0s: 长停顿，突出重点

3. 真实感提升:
   - 使用不同的 wpm 值模拟不同部分的打字速度
   - 添加适当的停顿和修正（backspace）
   - 模拟拼写错误和修正

4. 性能优化:
   - 对于长文本，使用 InsertTextAction 而非 TypeTextAction
   - 使用 play_with_frame_callback 时选择合适的 fps

5. 调试技巧:
   - 使用 InteractiveScheduler 进行步进调试
   - 使用 EventLogger 查看详细执行过程
   - 使用 ConsoleRenderer 可视化状态变化
"""
