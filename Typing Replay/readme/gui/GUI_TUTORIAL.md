# Typing Replay Engine - GUI 使用教程

欢迎使用 Typing Replay Engine 图形界面！本教程将帮助您快速上手。

## 📋 目录

1. [界面概览](#界面概览)
2. [快速开始](#快速开始)
3. [功能详解](#功能详解)
4. [实例演示](#实例演示)
5. [常见问题](#常见问题)
6. [快捷键](#快捷键)

---

## 界面概览

GUI 界面分为以下几个区域：

```
┌─────────────────────────────────────────────────┐
│  工具栏 (打开/保存/演示/帮助)                    │
├──────────────────┬──────────────────────────────┤
│                  │                              │
│  脚本编辑器      │   播放控制                   │
│  (JSON 格式)     │   - 实时预览                 │
│                  │   - 播放速度                 │
│                  │   - 播放/暂停/停止            │
│                  │   - 步进控制                 │
│                  │   - 进度条                   │
│                  │                              │
├──────────────────┴──────────────────────────────┤
│  状态栏 (消息 | 统计信息)                        │
└─────────────────────────────────────────────────┘
```

### 主要区域说明

1. **工具栏** - 顶部操作按钮
   - 📂 打开脚本：加载 JSON 脚本文件
   - 💾 保存脚本：保存当前脚本
   - 🎬 演示脚本：加载预设示例
   - 📖 帮助：查看使用说明

2. **脚本编辑器** - 左侧面板
   - 编写和编辑 JSON 格式的动作脚本
   - ✓ 验证脚本：检查格式是否正确
   - ⟲ 重置：恢复到默认脚本

3. **播放控制** - 右侧面板
   - **实时预览**：显示打字效果
   - **播放速度**：调整回放速度（0.1x - 3.0x）
   - **▶ 播放**：开始执行脚本
   - **⏸ 暂停**：暂停播放
   - **⏹ 停止**：停止并重置
   - **步进控制**：逐步执行动作

4. **状态栏** - 底部信息
   - 左侧：当前操作状态
   - 右侧：文本统计（行数、字符数、光标位置）

---

## 快速开始

### 第一步：运行 GUI

```bash
cd typing_replay
python gui.py
```

### 第二步：体验演示脚本

1. 点击 **🎬 演示脚本** 按钮
2. 选择 "Hello World - 基础示例"
3. 点击 **▶ 播放** 按钮
4. 观察右侧预览区的打字效果

### 第三步：尝试编辑脚本

在左侧编辑器中修改脚本：

```json
{
  "actions": [
    {"type": "type", "text": "你好，世界！", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n欢迎使用！", "wpm": 50}
  ]
}
```

点击 **✓ 验证脚本** 确认格式正确，然后 **▶ 播放**。

---

## 功能详解

### 1. 脚本格式

脚本使用 JSON 格式，包含一个 `actions` 数组：

```json
{
  "actions": [
    动作1,
    动作2,
    动作3
  ]
}
```

### 2. 支持的动作类型

#### 打字动作 (type)

模拟逐字符打字，支持速度控制。

```json
{
  "type": "type",
  "text": "要输入的文本",
  "wpm": 60
}
```

**参数说明：**
- `text`: 要打字的内容
- `wpm`: 每分钟单词数 (Words Per Minute)
  - 60 = 正常速度
  - 40 = 较慢（适合演示）
  - 80 = 较快（适合代码）

#### 即时插入 (insert)

不模拟打字过程，直接插入文本。

```json
{
  "type": "insert",
  "text": "立即出现的文本"
}
```

适合插入 Emoji 或大段文本。

#### 停顿 (pause)

添加延迟，模拟思考时间。

```json
{
  "type": "pause",
  "duration": 0.5
}
```

**参数说明：**
- `duration`: 停顿时长（秒）
  - 0.2-0.5 = 短暂停顿
  - 0.5-1.0 = 中等停顿
  - 1.0-2.0 = 长停顿

#### 退格删除 (backspace)

模拟按 Backspace 键。

```json
{
  "type": "backspace",
  "count": 5
}
```

**参数说明：**
- `count`: 删除的字符数

#### 光标移动 (move_cursor)

移动光标位置。

```json
{
  "type": "move_cursor",
  "position": 10
}
```

或使用相对偏移：

```json
{
  "type": "move_cursor",
  "offset": -5
}
```

#### 创建选区 (select)

选择一段文本。

```json
{
  "type": "select",
  "start": 0,
  "end": 5
}
```

选区创建后，下一次插入文本会替换选中内容。

#### 删除选区 (delete_selection)

删除当前选中的文本。

```json
{
  "type": "delete_selection"
}
```

### 3. 播放控制

#### 播放速度调节

- 拖动滑块调整速度
- 范围：0.1x（慢动作）到 3.0x（快进）
- 默认：1.0x（正常速度）

**使用场景：**
- 0.5x：详细演示，便于观察细节
- 1.0x：正常播放
- 2.0x：快速预览

#### 步进模式

适合调试和学习：

1. 点击 **▶ 下一步** 执行一个动作
2. 点击 **◀ 上一步** 回退一个动作
3. 观察每一步的变化

### 4. 验证脚本

点击 **✓ 验证脚本** 检查：
- JSON 格式是否正确
- 动作类型是否支持
- 参数是否完整

验证成功会显示动作总数。

---

## 实例演示

### 实例 1：简单打字

**场景**：模拟打招呼

```json
{
  "actions": [
    {"type": "type", "text": "Hello! ", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "How are you?", "wpm": 55}
  ]
}
```

**效果**：
1. 打字显示 "Hello! "
2. 停顿 0.5 秒
3. 继续打字 "How are you?"

---

### 实例 2：拼写修正

**场景**：模拟打错字并修正

```json
{
  "actions": [
    {"type": "type", "text": "The quikc brown fox", "wpm": 70},
    {"type": "pause", "duration": 0.8},
    {"type": "move_cursor", "position": 9},
    {"type": "backspace", "count": 5},
    {"type": "type", "text": "quick", "wpm": 65}
  ]
}
```

**效果**：
1. 打字 "The quikc brown fox"（拼写错误）
2. 停顿 0.8 秒（发现错误）
3. 移动光标到 "quikc" 后
4. 删除 "quikc"
5. 正确输入 "quick"

---

### 实例 3：文本替换

**场景**：选择并替换单词

```json
{
  "actions": [
    {"type": "type", "text": "I love JavaScript!", "wpm": 70},
    {"type": "pause", "duration": 0.5},
    {"type": "select", "start": 7, "end": 17},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "Python", "wpm": 65}
  ]
}
```

**效果**：
1. 打字 "I love JavaScript!"
2. 停顿
3. 选择 "JavaScript"
4. 停顿
5. 输入 "Python" 替换选区

---

### 实例 4：代码编写

**场景**：编写 Python 函数

```json
{
  "actions": [
    {"type": "type", "text": "def greet(name):", "wpm": 75},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n    return f\"Hello, {name}!\"", "wpm": 70},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n\nprint(greet(\"Alice\"))", "wpm": 75}
  ]
}
```

**效果**：
完整的函数定义和调用过程。

---

### 实例 5：Emoji 演示

**场景**：添加表情符号

```json
{
  "actions": [
    {"type": "type", "text": "Coding is fun! ", "wpm": 60},
    {"type": "insert", "text": "💻"},
    {"type": "pause", "duration": 0.2},
    {"type": "insert", "text": "🚀"},
    {"type": "pause", "duration": 0.2},
    {"type": "insert", "text": "✨"}
  ]
}
```

**效果**：
文字后依次出现三个 emoji。

---

### 实例 6：多段落文本

**场景**：创建多段落文档

```json
{
  "actions": [
    {"type": "type", "text": "# 标题\n\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "这是第一段内容。\n", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n这是第二段内容。", "wpm": 60}
  ]
}
```

---

### 实例 7：教程演示

**场景**：演示命令行操作

```json
{
  "actions": [
    {"type": "type", "text": "$ cd project", "wpm": 70},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n$ npm install", "wpm": 75},
    {"type": "pause", "duration": 1.0},
    {"type": "type", "text": "\n$ npm start", "wpm": 75},
    {"type": "pause", "duration": 0.5},
    {"type": "insert", "text": "\n🚀 Server started!"}
  ]
}
```

---

### 实例 8：创意写作

**场景**：展示创作过程

```json
{
  "actions": [
    {"type": "type", "text": "The night was dark", "wpm": 45},
    {"type": "pause", "duration": 1.5},
    {"type": "backspace", "count": 4},
    {"type": "type", "text": "quiet", "wpm": 40},
    {"type": "pause", "duration": 1.0},
    {"type": "type", "text": " and mysterious.", "wpm": 45}
  ]
}
```

---

## 常见问题

### Q1: 脚本验证失败怎么办？

**A:** 检查以下几点：
1. JSON 格式是否正确（括号、引号、逗号）
2. 动作类型拼写是否正确
3. 必需参数是否提供

使用在线 JSON 验证工具辅助检查。

### Q2: 如何控制打字速度？

**A:** 两种方式：
1. 修改脚本中的 `wpm` 参数（每分钟单词数）
2. 调整播放速度滑块（全局速度倍率）

推荐：
- 普通文本：50-60 WPM
- 代码：70-80 WPM
- 演示：40-50 WPM

### Q3: 中文或 Emoji 显示异常？

**A:** 
1. 确保脚本文件保存为 UTF-8 编码
2. 使用 `insert` 动作插入 Emoji
3. 检查字体是否支持显示的字符

### Q4: 播放时卡顿怎么办？

**A:** 
1. 减少动作数量
2. 使用 `insert` 代替 `type` 对于大段文本
3. 关闭其他占用资源的程序

### Q5: 如何制作循环播放？

**A:** 
GUI 暂不支持循环，可以：
1. 使用步进模式手动重复
2. 修改脚本代码添加循环逻辑

---

## 快捷键

### 编辑器
- `Ctrl + A`: 全选
- `Ctrl + C`: 复制
- `Ctrl + V`: 粘贴
- `Ctrl + Z`: 撤销

### 文件操作
- `Ctrl + O`: 打开文件（功能待绑定）
- `Ctrl + S`: 保存文件（功能待绑定）

### 播放控制
- `Space`: 播放/暂停（功能待绑定）

---

## 提示与技巧

### 💡 技巧 1: 模拟真实打字

```json
{
  "actions": [
    {"type": "type", "text": "import pandas as pd", "wpm": 75},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\nimport numpy", "wpm": 70},
    {"type": "pause", "duration": 0.2},
    {"type": "backspace", "count": 5},
    {"type": "type", "text": "numpy as np", "wpm": 65}
  ]
}
```

添加不同速度和偶尔的删除更真实。

### 💡 技巧 2: 突出重点

```json
{
  "actions": [
    {"type": "type", "text": "Regular text... ", "wpm": 60},
    {"type": "pause", "duration": 1.0},
    {"type": "type", "text": "IMPORTANT!", "wpm": 40},
    {"type": "pause", "duration": 1.5}
  ]
}
```

降低重要内容的打字速度并增加停顿。

### 💡 技巧 3: 使用步进调试

创建复杂脚本时：
1. 使用步进模式逐步执行
2. 验证每个动作的效果
3. 调整参数直到满意

### 💡 技巧 4: 保存常用脚本

将常用的脚本模板保存为文件：
- `greeting.json` - 问候语模板
- `code_demo.json` - 代码演示模板
- `tutorial.json` - 教程模板

---

## 下一步

- 📚 查看 [实例参考](EXAMPLES_GALLERY.md) 了解更多示例
- 🎓 阅读 [高级教程](ADVANCED_TUTORIAL.md) 学习高级技巧
- 💻 查看 [API 文档](README.md) 了解编程接口

---

**祝您使用愉快！** 🎉

如有问题，请查看项目文档或提交 Issue。
