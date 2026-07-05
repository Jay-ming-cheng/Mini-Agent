# Mini Agent

> 从零开始实现一个 Mini Agent，重点不是功能，而是理解 Agent Workflow 的设计思想。

---

## 📖 Project Goal

这个项目**不是为了实现一个复杂的 Agent**。

而是一步一步理解 Agent 的核心组成：

- Tool
- Planning
- Reflection
- Memory

以及这些 Workflow 是如何影响 Agent 行为的。

整个项目不会依赖 LangChain，而是基于 Python 从零实现，理解每一个模块为什么存在、为什么这样设计。

---

## 💻 Environment

- Python 3.10
- Windows 11

---

## 🚀 Development Principle

整个项目遵循统一的开发流程：

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

## 🗺️ Roadmap

- ✅ Step 1：Project Bootstrap
- ✅ Step 2：Configuration & LLM Client
- ✅ Step 3：Conversation Memory
- ✅ Step 4：Tool
- ✅  Step 5：Agent
- ⬜ Step 6：Planning
- ⬜ Step 7：Reflection
- ⬜ Step 8：Memory

---

## ✅ Current Progress

### Step 1：Project Bootstrap

完成项目初始化：

- 项目目录结构
- README
- docs
- `.gitignore`

---

### Step 2：Configuration & LLM Client

已完成：

- ✅ Config 模块
- ✅ LLMClient 封装
- ✅ OpenAI Compatible SDK
- ✅ Qwen API 接入
- ✅ 统一 `chat()` 接口
- ✅ 配置与业务解耦

### Step 3：Conversation Memory

已完成：

- ✅ 保存用户消息
- ✅ 保存模型回复
- ✅ 自动维护聊天上下文
- ✅ 支持连续多轮对话

现在已经可以：

```python
llm = LLMClient()

print(llm.chat("我叫 Jay"))
print(llm.chat("我叫什么？"))
```
模型能够根据历史对话回答问题。
### Step 4：Tool

已完成：

- ✅ 第一个 Tool（Calculator）
- ✅ Tool 与 LLM 解耦
- ✅ Tool 与 Agent 解耦
- ✅ Tool 独立测试
- ✅ Tool 异常处理
---
### Step 5: Agent

已完成：

- ✅ 新增 Agent 类
- ✅ Agent 成为系统统一入口
- ✅ Agent 与 LLMClient 解耦
- ✅ app.py 通过 Agent 与模型交互
## 📚 Documents

每一步都会记录完整的设计思路。

```
docs/
```

包括：

- 为什么需要？
- 为什么这样设计？
- Workflow 是什么？
- 学到了什么？