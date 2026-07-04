# LLM Client

---

# 本章目标

实现整个项目统一的大模型客户端（LLM Client）。

从这一章开始，整个 Mini Agent 不再直接调用 OpenAI SDK，而是统一通过 `LLMClient` 与大模型通信。

这样可以让上层模块无需关心底层模型是谁，也无需了解 SDK 的实现细节。

---

# 为什么需要 LLM Client？

假设没有 LLMClient。

那么每个模块都需要这样写：

```python
client = OpenAI(
    api_key=...,
    base_url=...
)

response = client.chat.completions.create(...)
```

随着项目越来越大：

- Planner
- Reflection
- Memory
- Tool
- Agent

都会依赖 OpenAI SDK。

这样会导致：

- 模块之间耦合严重
- 更换模型需要修改多个地方
- API 配置难以统一管理
- SDK 更换成本非常高

因此，我们需要增加一层抽象。

整个项目以后只依赖：

```python
llm.chat(...)
```

至于底层到底使用：

- OpenAI
- DeepSeek
- Qwen

对于业务层来说都是透明的。

---

# LLMClient 的职责

LLMClient 只负责一件事情：

> 与大模型通信。

负责：

- 创建 OpenAI Client
- 管理当前模型
- 向模型发送请求
- 返回统一格式的数据

不负责：

- Prompt Engineering
- Planning
- Reflection
- Memory
- Tool Calling

这些属于 Agent Workflow。

---

# 为什么设计成 Class？

LLMClient 不是一个简单的工具函数。

它需要维护自己的状态（State）。

例如：

```python
self.client
```

```python
self.model
```

因此更适合设计成一个对象。

```python
llm = LLMClient()
```

整个程序运行期间，只需要创建一次即可。

---

# 为什么在 __init__() 初始化 Client？

OpenAI Client 属于长期资源。

如果每次调用：

```python
llm.chat(...)
```

都重新创建：

```python
OpenAI(...)
```

不仅代码重复，也增加了维护成本。

因此：

Client 在对象创建时初始化一次。

之后整个生命周期都可以复用。

---

# 为什么 Model 不放到 OpenAI()？

OpenAI Client 的职责是建立通信。

真正选择模型是在发送请求的时候。

例如：

```python
response = self.client.chat.completions.create(
    model=self.model,
    messages=messages
)
```

因此：

Model 属于一次 Request。

而不是 Client。

这样以后同一个 Client 甚至可以调用不同模型。

---

# 为什么 messages 是 List？

OpenAI API 使用 messages 表示整个对话上下文。

例如：

```python
messages = [
    {
        "role": "user",
        "content": "你好"
    }
]
```

未来随着项目继续开发：

Memory 会保存历史消息。

Reflection 会修改 Prompt。

Planning 会添加新的上下文。

因此：

messages 会不断扩展。

它也是整个 Mini Agent 最重要的数据结构之一。

---

# 为什么 chat() 返回 str？

OpenAI SDK 返回的是一个复杂对象。

例如：

```python
response.choices[0].message.content
```

但是：

Planner

Reflection

Memory

Agent

都不应该了解 SDK 的结构。

因此：

LLMClient 应该负责解析返回结果。

统一返回：

```python
str
```

以后即使底层 SDK 发生变化，上层代码也无需修改。

---

# Workflow

```
Agent
      │
      ▼
Planner / Reflection / Memory
      │
      ▼
LLMClient
      │
      ▼
OpenAI Compatible SDK
      │
      ▼
Qwen / DeepSeek / OpenAI
```

LLMClient 是整个项目唯一允许直接访问大模型的模块。

---

# 本章总结

本章完成了 Mini Agent 第一层抽象。

实现了统一的大模型调用入口：

```python
llm = LLMClient()

response = llm.chat("你好")
```

以后：

- Planner
- Reflection
- Tool
- Memory

都会通过：

```python
llm.chat(...)
```

完成与大模型的交互，而不会直接依赖任何 SDK。

这也是整个 Agent Workflow 的基础。

---

# 学到了什么？

- 为什么需要 LLMClient？
- 为什么要封装 OpenAI SDK？
- 为什么使用 Class 而不是函数？
- 为什么 Client 在 `__init__()` 中初始化？
- 为什么 `messages` 是整个 Agent 最重要的数据结构？
- 为什么统一返回 `str` 而不是 SDK 对象？

这些设计思想比代码本身更加重要，也是后续实现 Agent Workflow 的基础。