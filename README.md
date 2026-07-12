# Mini Agent

> A lightweight AI Agent built from scratch with Python.

> 从零实现一个 Mini Agent，不依赖 LangChain，重点理解 Agent Workflow（Planning、ReAct、Reflection、Memory）的设计思想。

---

# 📖 Project Goal

这个项目**不是为了实现一个复杂的 Agent**。

而是一步一步理解 Agent 的核心组成：

- Tool
- Planning
- ReAct
- Reflection
- Memory

以及这些 Workflow 是如何影响 Agent 行为的。

整个项目不会依赖 LangChain，而是基于 Python 从零实现，理解每一个模块为什么存在、为什么这样设计。

---

# 💻 Environment

- Python 3.10+
- Windows 11
- OpenAI Compatible API

---

# 🚀 Development Principle

整个项目遵循统一开发流程：

```text
Design
    ↓
Coding
    ↓
Test
    ↓
README
    ↓
Docs
    ↓
Commit
    ↓
Push
```

每完成一个模块，都先完成设计，再编码、测试，并记录设计思考。

---

# 🏗 Architecture

当前版本采用 **ReAct Workflow**。

```text
                User
                  │
                  ▼
              Agent.chat()
                  │
                  ▼
              _reason()
                  │
                  ▼
             LLM Decision
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
     Finish             Execute Action
        │                   │
        │                   ▼
        │              Tool.run()
        │                   │
        │                   ▼
        │             Observation
        │                   │
        └────────── Loop ───┘
```

---

# 🗺 Roadmap

- ✅ Step 1：Project Bootstrap
- ✅ Step 2：Configuration & LLM Client
- ✅ Step 3：Conversation Memory
- ✅ Step 4：Tool
- ✅ Step 5：Agent
- ✅ Step 6：Tool Workflow
- ✅ Step 7：Planning
- ✅ Step 8：ReAct
- ✅ Step 9：Reflection
- ⬜ Step 10：Memory

---

# ✅ Current Progress

## Step 1：Project Bootstrap

已完成：

- ✅ 项目目录结构
- ✅ README
- ✅ docs
- ✅ `.gitignore`

---

## Step 2：Configuration & LLM Client

已完成：

- ✅ Config 模块
- ✅ LLMClient 封装
- ✅ OpenAI Compatible SDK
- ✅ Qwen API 接入
- ✅ 统一 `chat()` 接口
- ✅ 配置与业务解耦

---

## Step 3：Conversation Memory

已完成：

- ✅ 保存用户消息
- ✅ 保存模型回复
- ✅ 自动维护聊天上下文
- ✅ 支持连续多轮对话

示例：

```python
llm = LLMClient()

print(llm.chat("我叫 Jay"))
print(llm.chat("我叫什么？"))
```

模型能够根据历史聊天回答问题。

---

## Step 4：Tool

已完成：

- ✅ Calculator Tool
- ✅ Tool 与 LLM 解耦
- ✅ Tool 与 Agent 解耦
- ✅ Tool 独立测试
- ✅ Tool 异常处理

---

## Step 5：Agent

已完成：

- ✅ 新增 Agent 类
- ✅ Agent 成为系统统一入口
- ✅ Agent 与 LLMClient 解耦
- ✅ app.py 统一通过 Agent 与模型交互

---

## Step 6：Tool Workflow

已完成：

- ✅ Agent 判断是否需要调用 Tool
- ✅ LLM 输出 Tool Decision（JSON）
- ✅ Agent 解析 Tool Decision
- ✅ Agent 调用 Tool
- ✅ Tool 返回执行结果
- ✅ LLM 基于 Tool Result 生成最终回复
- ✅ 内部 Prompt 不污染聊天历史

---

## Step 7：Planning

已完成：

- ✅ 新增 Planner（`_plan()`）
- ✅ LLM 生成执行计划（Plan）
- ✅ Plan 使用 JSON 数组表示
- ✅ Agent 根据 Plan 执行 Tool
- ✅ Tool Decision 升级为 Planning
- ✅ Planning Prompt 不保存聊天历史

---

## Step 8：ReAct

已完成：

- ✅ ReAct Prompt
- ✅ Observation 管理
- ✅ `_reason()`
- ✅ `_execute_action()`
- ✅ ReAct Loop
- ✅ Multi-step Reasoning

当前 Agent 已从一次性 Planning 升级为经典 **ReAct Workflow**。

Agent 会根据 Observation 不断进行：

```text
Reason
    ↓
Action
    ↓
Observation
    ↓
Reason
```

直到完成整个任务。

### Step 9：Reflection

已完成：

- ✅ 新增 Reflection Agent（_reflect）
- ✅ Reflection Prompt
- ✅ Tool Result 分析
- ✅ Reflection JSON 输出
- ✅ Reflection 接入 ReAct Loop
- ✅ Observation + Reflection 共同参与下一轮推理
---

# 🚀 Quick Start

克隆项目：

```bash
git clone https://github.com/Jay-ming-cheng/Mini-Agent.git
```

进入项目：

```bash
cd Mini-Agent
```

安装依赖：

```bash
pip install -r requirements.txt
```

运行：

```bash
python app.py
```

---

# 📚 Documents

所有设计文档均位于：

```text
docs/
├── 01-Architecture.md
├── 02-LLM.md
├── 03-LLMClient.md
├── 04-ConversationMemory.md
├── 05-Tool.md
├── 06-Agent.md
├── 07-ToolWorkflow.md
├── 08-planning-workflow.md
└── 09-react-workflow.md (Coming Soon)
```

每篇文档都会记录：

- 为什么需要？
- 为什么这样设计？
- Workflow 是什么？
- 学到了什么？

---

# 🔮 Future Plan

下一阶段计划实现：

- Reflection
- Memory
- Multi-Tool
- Search Tool
- Browser Tool
- Multi-Agent

---

> 本项目重点不是实现一个功能丰富的 Agent，而是通过从零实现各个模块，深入理解现代 AI Agent 的工作原理与设计思想。