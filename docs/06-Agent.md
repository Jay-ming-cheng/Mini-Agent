# Agent

## 为什么需要 Agent？

LLM 只能负责生成文本。

如果未来需要：

- Tool
- Planning
- Reflection
- Memory

这些能力都直接写进 LLMClient，会导致职责越来越多，模块越来越臃肿。

因此，需要一个新的模块统一组织整个 Workflow。

Agent 的职责不是生成内容，而是协调整个系统完成任务。

---

## Agent 与 LLMClient 的区别

### LLMClient

职责：

- 与大模型通信
- 屏蔽不同模型 SDK 的差异
- 提供统一的 chat() 接口
- 管理当前会话消息（Conversation Memory）

LLMClient 不负责：

- Tool 调度
- Planning
- Reflection
- 长期 Memory

---

### Agent

职责：

- 作为整个系统的统一入口
- 接收用户请求
- 调用 LLM
- 调用 Tool（后续实现）
- 组织整个 Workflow

Agent 不负责：

- 与模型底层通信
- Tool 的具体实现
- 长期 Memory 管理

---

## 当前 Workflow

目前 Agent 的工作流程非常简单：

```
User
    │
    ▼
Agent
    │
    ▼
LLMClient
    │
    ▼
LLM
```

Agent 目前只是统一入口。

后续会逐渐增加：

- Tool
- Planning
- Reflection
- Memory

最终形成真正的 Agent Workflow。

---

## 为什么 Agent 不直接实现 Tool？

Tool 属于独立模块。

Agent 的职责是：

- 判断是否需要 Tool
- 决定调用哪个 Tool
- 获取 Tool 返回结果

而不是实现 Tool 本身。

这样能够保持模块职责清晰，降低耦合。

---

## 当前版本为什么没有 Thinking？

目前 Agent 只是将用户请求转发给 LLM。

它还没有进行任何决策。

因此，不应该人为输出：

```
Thinking...
```

只有当 Agent 真正开始：

- 判断
- 决策
- 调度 Tool

时，才算真正进行了 "Thinking"。

不要伪造系统当前并不存在的能力。

---

## 学到的知识

### 1. Agent 是 Workflow，而不是 LLM

LLM 负责生成语言。

Agent 负责组织整个工作流程。

Agent 并不会提升模型本身的能力，而是协调不同模块，让整个系统能够完成更加复杂的任务。

---

### 2. 单一职责原则（SRP）

LLMClient 负责模型通信。

Tool 负责工具能力。

Agent 负责 Workflow。

每个模块只负责一件事情。

---

### 3. 依赖注入（Dependency Injection）

Agent 不负责创建 LLMClient。

创建对象由外部完成，再传入 Agent。

这样能够降低耦合，提高可维护性。

例如：

```python
llm = LLMClient()
agent = Agent(llm)
```

---

### 4. YAGNI

当前版本只有一个 LLMClient。

因此没有提前设计：

- BaseLLM
- Interface
- Factory

避免为了未来可能存在的需求增加复杂度。

每一版只解决当前的问题。

---

## 本章总结

本章实现了系统中的第一个 Agent。

虽然当前 Agent 只是统一入口，但已经完成了整个系统架构的重要调整。

后续所有能力，包括：

- Tool
- Planning
- Reflection
- Memory

都将在 Agent 中逐步实现，而无需修改外部调用方式。

这也是整个 Mini Agent 项目正式进入 Workflow 阶段的开始。