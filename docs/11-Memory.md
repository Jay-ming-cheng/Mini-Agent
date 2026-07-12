# 11 - Memory

## 为什么需要 Memory？

在完成 Reflection 后，Agent 已经可以：

- 调用 Tool
- 根据 Observation 推理
- 根据 Reflection 调整下一步行动

但是 Agent 仍然存在一个明显的问题：

> 它不会记住用户。

例如：

```text
You:
我叫 Jay

Agent:
你好，Jay！
```

下一轮：

```text
You:
我叫什么？
```

如果没有 Memory，Agent 无法回答。

原因是：

当前项目中的 Conversation History 只负责维护当前聊天上下文，而不是长期保存用户信息。

因此，我们需要一个新的模块：

> Memory。

---

# Conversation History ≠ Memory

很多刚接触 Agent 的时候，会认为：

> 聊天记录就是 Memory。

实际上两者完全不同。

Conversation History：

- 保存完整聊天内容
- 服务于当前对话
- 会越来越长
- 更多属于上下文(Context)

例如：

```text
User:
你好

Assistant:
你好

User:
今天天气怎么样？
```

这些内容一般不会长期保存。

---

Memory：

只保存长期有价值的信息。

例如：

```text
姓名

年龄

职业

城市

兴趣

偏好
```

例如：

```json
{
    "name": "Jay",
    "city": "重庆"
}
```

Memory 更像用户画像，而不是聊天记录。

---

# Memory Workflow

Memory 在整个 Agent Workflow 中主要负责两件事情：

```text
Retrieve Memory

↓

Store Memory
```

因此完整流程变成：

```text
User

↓

Retrieve Memory

↓

Reason

↓

Action

↓

Observation

↓

Reflection

↓

Reason

↓

Finish

↓

Extract Memory

↓

Store Memory
```

Memory 不参与推理。

Memory 只是给 Reason 提供更多背景信息。

---

# Retrieve Memory

每次用户发送新的消息时，

Agent 首先读取长期 Memory：

```python
memory = self.memory.get_all()
```

然后加入 Prompt：

```text
Memory:

name: Jay

city: 重庆
```

LLM 在推理之前，就已经知道用户是谁。

因此：

```text
You:
我叫什么？
```

模型可以回答：

```text
你叫 Jay。
```

---

# Store Memory

真正困难的不是保存。

而是：

> 保存什么？

一种简单的方法是：

```python
if "我叫" in message:
    ...
```

但是这种方式无法扩展。

例如：

```text
我的名字叫 Jay

我是 Jay

以后叫我 Jay
```

都会失败。

因此本项目仍然采用 LLM 完成 Memory 提取。

新增：

```python
_extract_memory()
```

职责：

根据用户输入，

判断是否存在值得长期保存的信息。

例如：

```text
用户：

我叫 Jay
```

LLM 返回：

```json
{
    "save": true,
    "key": "name",
    "value": "Jay"
}
```

随后：

```python
memory.save(
    key,
    value
)
```

完成 Memory 更新。

---

# Memory 数据结构

第一版 Memory 并没有采用数据库。

而是使用 Python Dict：

```python
{
    "name":"Jay",
    "city":"重庆"
}
```

对应接口：

```python
save()

load()

get_all()
```

这样做的目的不是追求完整功能，

而是先理解 Memory Workflow。

后续可以很容易替换成：

- SQLite
- Redis
- Vector Database

而无需修改 Agent。

---

# 为什么 Memory 独立出来？

Memory 不属于：

- Tool
- Reason
- Reflection

因为它负责的是：

> 长期知识管理。

如果直接放到 Agent 中，

Agent 会承担越来越多职责。

因此：

```text
Agent

↓

Memory
```

采用模块化设计，

可以保持各模块职责单一，方便后续扩展。

---

# 本模块收获

完成 Memory 模块后，

Mini Agent 已经具备现代 Agent 的核心 Workflow：

- Tool
- Planning
- ReAct
- Reflection
- Memory

同时，我也理解了：

- Conversation History 与 Memory 的区别
- Memory 的核心不是存储，而是管理长期知识
- LLM 不仅可以回答问题，也可以帮助提取长期信息
- Memory Workflow 包括 Retrieve 与 Store 两部分
- Prompt 中引入 Memory，可以显著增强 Agent 的持续对话能力

---

# 下一步

完成 Mini Agent v1.0 后，

下一阶段将继续学习：

- Agentic RAG
- MCP（Model Context Protocol）
- Multi-Agent
- Enterprise AI Agent

进一步理解企业级 AI Agent 的设计与实现。