# Typing Replay Engine - 实例参考库

这是一个精心整理的脚本实例集合，涵盖各种使用场景。每个实例都可以直接在 GUI 中使用。

## 📚 目录

1. [基础实例](#基础实例)
2. [编程场景](#编程场景)
3. [文档编写](#文档编写)
4. [教学演示](#教学演示)
5. [创意应用](#创意应用)
6. [实用工具](#实用工具)

---

## 基础实例

### 实例 1: Hello World

**描述**: 最简单的打字演示

```json
{
  "actions": [
    {"type": "type", "text": "Hello, World!", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n欢迎使用 Typing Replay Engine!", "wpm": 55}
  ]
}
```

**适用场景**: 
- 快速测试
- 新手入门
- 功能演示

---

### 实例 2: 打字修正

**描述**: 模拟打错字并修正

```json
{
  "actions": [
    {"type": "type", "text": "The quick borwn fox", "wpm": 70},
    {"type": "pause", "duration": 0.8},
    {"type": "move_cursor", "position": 14},
    {"type": "backspace", "count": 5},
    {"type": "type", "text": "brown", "wpm": 65},
    {"type": "move_cursor", "position": 19},
    {"type": "type", "text": " jumps over the lazy dog.", "wpm": 70}
  ]
}
```

**学习要点**:
- 光标移动
- 退格删除
- 错误修正流程

---

### 实例 3: 文本选择与替换

**描述**: 选中文本并替换

```json
{
  "actions": [
    {"type": "type", "text": "I love programming in Java.", "wpm": 65},
    {"type": "pause", "duration": 0.5},
    {"type": "select", "start": 22, "end": 26},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "Python", "wpm": 60}
  ]
}
```

**学习要点**:
- 创建选区
- 选区自动替换
- 位置计算

---

### 实例 4: 多行文本

**描述**: 创建多段落内容

```json
{
  "actions": [
    {"type": "type", "text": "第一行文本", "wpm": 60},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n第二行文本", "wpm": 60},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n第三行文本", "wpm": 60}
  ]
}
```

**学习要点**:
- 换行符 `\n` 的使用
- 多段落组织

---

### 实例 5: Emoji 表情

**描述**: 添加表情符号

```json
{
  "actions": [
    {"type": "type", "text": "今天心情不错 ", "wpm": 60},
    {"type": "insert", "text": "😊"},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n工作进展顺利 ", "wpm": 60},
    {"type": "insert", "text": "💪"},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n期待周末 ", "wpm": 60},
    {"type": "insert", "text": "🎉"}
  ]
}
```

**学习要点**:
- `insert` 用于 emoji
- emoji 不计入 WPM

---

## 编程场景

### 实例 6: Python 函数

**描述**: 编写 Python 函数

```json
{
  "actions": [
    {"type": "type", "text": "def calculate_sum(numbers):", "wpm": 75},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n    \"\"\"计算数字列表的总和\"\"\"", "wpm": 70},
    {"type": "pause", "duration": 0.4},
    {"type": "type", "text": "\n    total = 0", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n    for num in numbers:", "wpm": 75},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n        total += num", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n    return total", "wpm": 75}
  ]
}
```

**适用场景**:
- 编程教学
- 代码演示
- 算法讲解

---

### 实例 7: JavaScript 类

**描述**: 创建 ES6 类

```json
{
  "actions": [
    {"type": "type", "text": "class Person {", "wpm": 80},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n  constructor(name, age) {", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n    this.name = name;", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n    this.age = age;", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n  }", "wpm": 80},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\n  greet() {", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n    console.log(`Hi, I'm ${this.name}`);", "wpm": 70},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n  }", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n}", "wpm": 80}
  ]
}
```

---

### 实例 8: SQL 查询

**描述**: 编写 SQL 查询语句

```json
{
  "actions": [
    {"type": "type", "text": "SELECT ", "wpm": 70},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "users.name, orders.total", "wpm": 75},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\nFROM users", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\nJOIN orders ON users.id = orders.user_id", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "\nWHERE orders.total > 100", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\nORDER BY orders.total DESC;", "wpm": 75}
  ]
}
```

---

### 实例 9: Git 命令

**描述**: 演示 Git 工作流

```json
{
  "actions": [
    {"type": "type", "text": "$ git add .", "wpm": 80},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n$ git commit -m \"Add new feature\"", "wpm": 75},
    {"type": "pause", "duration": 0.8},
    {"type": "type", "text": "\n$ git push origin main", "wpm": 80},
    {"type": "pause", "duration": 0.5},
    {"type": "insert", "text": "\n✓ Changes pushed successfully!"}
  ]
}
```

---

### 实例 10: HTML 结构

**描述**: 创建 HTML 页面

```json
{
  "actions": [
    {"type": "type", "text": "<!DOCTYPE html>", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n<html lang=\"zh-CN\">", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n<head>", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n  <title>我的网页</title>", "wpm": 70},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n</head>", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n<body>", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n  <h1>Hello World</h1>", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n</body>", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "\n</html>", "wpm": 80}
  ]
}
```

---

## 文档编写

### 实例 11: Markdown 文档

**描述**: 编写 Markdown 格式文档

```json
{
  "actions": [
    {"type": "type", "text": "# 项目说明\n\n", "wpm": 70},
    {"type": "pause", "duration": 0.4},
    {"type": "type", "text": "## 简介\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "这是一个示例项目。\n\n", "wpm": 60},
    {"type": "pause", "duration": 0.4},
    {"type": "type", "text": "## 特性\n\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "- 功能强大\n", "wpm": 60},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "- 易于使用\n", "wpm": 60},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "- 开源免费", "wpm": 60}
  ]
}
```

---

### 实例 12: 博客文章

**描述**: 撰写博客文章

```json
{
  "actions": [
    {"type": "type", "text": "# 如何学习编程\n\n", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "学习编程是一个循序渐进的过程。", "wpm": 55},
    {"type": "pause", "duration": 0.8},
    {"type": "type", "text": "首先，选择一门合适的编程语言...", "wpm": 55},
    {"type": "pause", "duration": 1.0},
    {"type": "backspace", "count": 3},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "。", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n\n接下来，需要大量的练习。", "wpm": 55}
  ]
}
```

---

### 实例 13: 技术文档

**描述**: 编写 API 文档

```json
{
  "actions": [
    {"type": "type", "text": "## API 端点\n\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "### GET /api/users\n\n", "wpm": 75},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "获取用户列表。\n\n", "wpm": 60},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "**参数:**\n", "wpm": 70},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "- `page`: 页码（可选）\n", "wpm": 65},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "- `limit`: 每页数量（可选）\n\n", "wpm": 65},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "**响应:**\n", "wpm": 70},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "```json\n{\n  \"users\": [...]\n}\n```", "wpm": 70}
  ]
}
```

---

## 教学演示

### 实例 14: 数学公式

**描述**: 展示数学推导

```json
{
  "actions": [
    {"type": "type", "text": "勾股定理：\n", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "a² + b² = c²", "wpm": 50},
    {"type": "pause", "duration": 1.0},
    {"type": "type", "text": "\n\n其中：\n", "wpm": 60},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "- a, b 为直角边\n", "wpm": 55},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "- c 为斜边", "wpm": 55}
  ]
}
```

---

### 实例 15: 步骤说明

**描述**: 分步教学

```json
{
  "actions": [
    {"type": "type", "text": "如何泡一杯完美的咖啡：\n\n", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "步骤 1: 准备咖啡豆和磨豆机", "wpm": 55},
    {"type": "pause", "duration": 0.8},
    {"type": "type", "text": "\n步骤 2: 研磨至合适的粗细", "wpm": 55},
    {"type": "pause", "duration": 0.8},
    {"type": "type", "text": "\n步骤 3: 加热水至 92-96°C", "wpm": 55},
    {"type": "pause", "duration": 0.8},
    {"type": "type", "text": "\n步骤 4: 冲泡并享用 ", "wpm": 55},
    {"type": "insert", "text": "☕"}
  ]
}
```

---

### 实例 16: 命令行教程

**描述**: Linux 命令演示

```json
{
  "actions": [
    {"type": "type", "text": "# 创建新目录\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "$ mkdir my-project", "wpm": 75},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n\n# 进入目录\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "$ cd my-project", "wpm": 75},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "\n\n# 初始化项目\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "$ npm init -y", "wpm": 75}
  ]
}
```

---

## 创意应用

### 实例 17: 诗歌创作

**描述**: 展示诗歌写作过程

```json
{
  "actions": [
    {"type": "type", "text": "静夜思\n\n", "wpm": 50},
    {"type": "pause", "duration": 1.0},
    {"type": "type", "text": "床前明月光，", "wpm": 45},
    {"type": "pause", "duration": 1.5},
    {"type": "type", "text": "\n疑是地上霜。", "wpm": 45},
    {"type": "pause", "duration": 1.5},
    {"type": "type", "text": "\n举头望明月，", "wpm": 45},
    {"type": "pause", "duration": 1.5},
    {"type": "type", "text": "\n低头思故乡。", "wpm": 45}
  ]
}
```

---

### 实例 18: 故事叙述

**描述**: 讲述故事

```json
{
  "actions": [
    {"type": "type", "text": "很久很久以前", "wpm": 50},
    {"type": "pause", "duration": 1.0},
    {"type": "backspace", "count": 7},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "从前", "wpm": 50},
    {"type": "pause", "duration": 0.8},
    {"type": "type", "text": "，有一个勇敢的骑士...", "wpm": 48},
    {"type": "pause", "duration": 1.5},
    {"type": "type", "text": "\n\n他踏上了寻找真理的旅程。", "wpm": 50}
  ]
}
```

---

### 实例 19: 聊天对话

**描述**: 模拟聊天界面

```json
{
  "actions": [
    {"type": "type", "text": "Alice: 你好！", "wpm": 60},
    {"type": "pause", "duration": 1.0},
    {"type": "type", "text": "\nBob: 嗨，Alice！最近怎么样？", "wpm": 65},
    {"type": "pause", "duration": 1.5},
    {"type": "type", "text": "\nAlice: 很好！刚完成了一个项目。", "wpm": 60},
    {"type": "pause", "duration": 1.5},
    {"type": "type", "text": "\nBob: 太棒了！", "wpm": 65},
    {"type": "insert", "text": " 🎉"}
  ]
}
```

---

## 实用工具

### 实例 20: 待办清单

**描述**: 创建任务列表

```json
{
  "actions": [
    {"type": "type", "text": "今日待办：\n\n", "wpm": 60},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "☐ 回复邮件\n", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "☐ 完成报告\n", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "☐ 团队会议\n", "wpm": 60},
    {"type": "pause", "duration": 0.5},
    {"type": "type", "text": "☑ 代码审查", "wpm": 60}
  ]
}
```

---

### 实例 21: 会议记录

**描述**: 记录会议要点

```json
{
  "actions": [
    {"type": "type", "text": "会议记录 - 2024/01/15\n\n", "wpm": 70},
    {"type": "pause", "duration": 0.4},
    {"type": "type", "text": "参会人员：张三、李四、王五\n\n", "wpm": 65},
    {"type": "pause", "duration": 0.4},
    {"type": "type", "text": "讨论议题：\n", "wpm": 70},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "1. 项目进度更新\n", "wpm": 65},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "2. 下周计划\n", "wpm": 65},
    {"type": "pause", "duration": 0.3},
    {"type": "type", "text": "3. 风险评估", "wpm": 65}
  ]
}
```

---

### 实例 22: 配置文件

**描述**: 编写 JSON 配置

```json
{
  "actions": [
    {"type": "type", "text": "{\n", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "  \"name\": \"my-app\",\n", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "  \"version\": \"1.0.0\",\n", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "  \"dependencies\": {\n", "wpm": 75},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "    \"react\": \"^18.0.0\"\n", "wpm": 70},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "  }\n", "wpm": 80},
    {"type": "pause", "duration": 0.2},
    {"type": "type", "text": "}", "wpm": 80}
  ]
}
```

---

## 💡 使用建议

### 1. 调整速度

根据内容类型调整 WPM：
- **普通文本**: 50-60
- **代码**: 70-80
- **命令**: 75-85
- **创意写作**: 40-50

### 2. 合理停顿

- 句子结束：0.3-0.5 秒
- 段落结束：0.5-1.0 秒
- 思考过程：1.0-2.0 秒

### 3. 模拟真实

- 偶尔添加拼写错误和修正
- 使用不同的速度
- 适当使用选择和替换

### 4. 保存模板

将常用脚本保存为文件：
```
templates/
  ├── greeting.json
  ├── code-demo.json
  ├── blog-post.json
  └── tutorial.json
```

---

## 📥 下载示例

所有示例都可以从以下位置下载：

1. GUI 内置演示脚本
2. `demo_script.json` 文件
3. 项目 GitHub 仓库

---

## 🎯 下一步

- 尝试组合多个示例
- 创建自己的脚本库
- 分享你的创意脚本

**祝您创作愉快！** 🎨
