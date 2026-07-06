# Tool Workflow

## Why

前面的章节已经完成了：

- LLMClient
- Conversation Memory
- Tool
- Agent

但是 Agent 仍然只是把用户消息直接发送给 LLM。

真正的 Agent 应该能够：

1. 判断是否需要调用 Tool
2. 调用 Tool
3. 使用 Tool 的结果回答用户

因此，本章实现第一个完整的 Agent Workflow。

---

## Workflow

整个流程如下：

```text
User
    │
    ▼
Agent
    │
    ▼
LLM（Tool Decision）
    │
    ▼
JSON
    │
    ▼
Agent
    │
    ▼
Tool
    │
    ▼
Tool Result
    │
    ▼
LLM（Generate Response）
    │
    ▼
User
```

---

## Tool Decision

Agent 首先调用 LLM。

Prompt 要求模型输出：

```json
{
    "tool": "calculator",
    "expression": "(23+99)*8"
}
```

如果无需 Tool，则返回：

```text
NONE
```

Agent 根据结果决定是否调用 Tool。

---

## Tool Execution

如果需要 Tool：

Agent 根据 Tool 名称找到对应 Tool。

例如：

```python
tool = self.tools["calculator"]
```

然后执行：

```python
tool.run(expression)
```

Tool 只负责完成自己的专业能力。

例如：

Calculator 只负责计算表达式。

---

## Generate Response

Tool 返回结果后：

Agent 再次调用 LLM。

Prompt 中包含：

- 用户问题
- Tool 返回结果

LLM 根据 Tool 返回结果组织自然语言回复。

例如：

```text
用户：

计算 (23+99)*8

Tool：

976
```

最终回复：

```text
(23+99)*8 的计算结果是 976。
```

---

## Design Principles

整个 Workflow 遵循职责分离原则。

### LLMClient

负责：

- 与模型通信

不负责：

- Tool
- Workflow
- Prompt Design

---

### Tool

负责：

自己的专业能力。

例如：

Calculator：

输入：

```text
(23+99)*8
```

输出：

```text
976
```

不负责自然语言生成。

---

### Agent

负责整个 Workflow：

- Tool Decision
- Tool Execution
- Response Generation

Agent 是整个系统的协调者。

---

## Conversation History

本章新增了一个重要设计。

LLM 的调用分为两种：

### User Conversation

保存聊天记录。

例如：

```python
llm.chat(message)
```

---

### Internal Prompt

不保存聊天记录。

例如：

- Tool Decision
- Generate Response
- Planning（未来）
- Reflection（未来）

因此，LLMClient 新增：

```python
save_history=False
```

用于避免内部 Prompt 污染聊天历史。

---

## Current Limitations

当前版本仍有一些限制：

- 仅支持 Calculator
- Tool Decision 依赖 Prompt
- 不支持多个 Tool
- 不支持 Tool Chain
- 不支持自动参数解析
- 不支持 Function Calling

这些能力将在后续章节逐步实现。

---

## Summary

本章完成了第一个真正意义上的 Agent。

Agent 已经具备：

- Tool Decision
- Tool Execution
- Response Generation

整个系统已经能够根据用户请求自主决定是否调用 Tool，并结合 Tool 返回结果生成最终回复。

这是整个 Mini-Agent 项目的第一个完整 Workflow。