# Conversation Memory

---

# 本章目标

实现 Mini Agent 的第一版 **Conversation Memory（对话记忆）**。

在上一章中，我们已经能够调用大模型完成一次对话。

但是，每次调用 `chat()` 都是一段全新的对话，模型无法记住上一轮聊天内容。

本章的目标就是让 Agent 拥有**短期记忆**，支持连续多轮对话。

---

# 为什么需要 Conversation Memory？

如果每次调用模型时都重新创建：

```python
messages = [
    {
        "role": "user",
        "content": message
    }
]
```

那么模型收到的永远只有当前这一句话。

例如：

```
用户：你好

AI：你好！

用户：我刚才说了什么？
```

第二次请求发送给模型的是：

```python
[
    {
        "role": "user",
        "content": "我刚才说了什么？"
    }
]
```

模型根本不知道第一轮发生了什么。

因此，它无法完成真正的聊天。

---

# Workflow

Conversation Memory 的核心思想非常简单：

持续维护整个对话历史（messages）。

```
用户输入
      │
      ▼
保存 User Message
      │
      ▼
发送 messages 给 LLM
      │
      ▼
获得 Assistant 回复
      │
      ▼
保存 Assistant Message
      │
      ▼
返回结果
```

整个 Workflow 可以表示为：

```
User
   │
   ▼
messages + User
   │
   ▼
LLM
   │
   ▼
Assistant
   │
   ▼
messages + Assistant
   │
   ▼
Return
```

随着聊天继续进行，`messages` 会不断增长。

例如：

```python
[
    {
        "role": "user",
        "content": "你好"
    },
    {
        "role": "assistant",
        "content": "你好！"
    },
    {
        "role": "user",
        "content": "我叫什么？"
    }
]
```

这样模型就能够看到完整的聊天上下文。

---

# Coding

本章主要完成三个修改。

## 1. 在 LLMClient 中维护聊天记录

新增：

```python
self.messages = []
```

聊天记录属于 LLMClient 的状态（State），因此放在对象内部维护，而不是每次调用重新创建。

---

## 2. 保存用户消息

每次用户发送新的问题时：

```python
self.messages.append(
    {
        "role": "user",
        "content": message
    }
)
```

随后，将完整的 `messages` 发送给大模型。

---

## 3. 保存模型回复

模型返回结果后：

```python
self.messages.append(
    {
        "role": "assistant",
        "content": assistant_message
    }
)
```

这样下一轮聊天时，模型能够看到完整的历史记录。

---

# 为什么这样设计？

## 为什么使用 self.messages？

聊天记录属于整个会话（Conversation）的状态。

如果放在：

```python
chat()
```

内部，每次调用都会重新创建。

因此必须作为：

```python
self.messages
```

由对象统一维护。

---

## 为什么既保存 User，也保存 Assistant？

完整的聊天不仅包括用户的问题，也包括模型的回答。

如果只保存：

```text
User
↓

User
```

模型将无法知道上一轮自己回答了什么。

因此必须保存完整对话。

---

## 为什么先保存 User，再调用模型？

模型只能看到发送给它的内容。

因此必须：

```
保存 User
    ↓
发送给模型
    ↓
获得回复
```

如果先调用模型，再保存用户消息，那么模型实际上没有收到当前问题。

---

# 本章踩坑

## ❌ 踩坑一

### 最开始认为

应该先调用模型，再保存用户消息。

### 为什么这样想？

认为聊天记录只是为了记录历史。

### 最终理解

聊天记录不仅用于保存历史，更是模型生成回复的输入。

因此必须：

```
保存 User
    ↓
调用模型
```

顺序不能反。

---

## ❌ 踩坑二

### 最开始认为

Memory 保存的是未来有价值的信息。

### 为什么这样想？

把 Conversation Memory 和 Long-term Memory 混淆了。

### 最终理解

Conversation Memory：

维护当前聊天上下文。

Long-term Memory：**
**
保存真正长期有价值的信息。

两者属于不同层次的 Memory。

---

# 本章总结

本章完成了 Mini Agent 第一版 Conversation Memory。

实现后：

- 能够保存用户消息
- 能够保存模型回复
- 支持连续多轮聊天
- 模型能够理解聊天上下文

Conversation Memory 并没有使用数据库。

它的本质只是持续维护：

```python
messages
```

这也是整个 Agent Workflow 最核心的数据结构。

---

# 学到了什么？

- 什么是 Conversation Memory？
- 为什么聊天记录属于对象状态（State）？
- 为什么要维护 `self.messages`？
- 为什么需要同时保存 User 和 Assistant？
- 为什么先保存 User，再请求模型？
- Conversation Memory 与 Long-term Memory 的区别。

---

# 下一章

目前 Agent 已经具备：

- ✅ LLM
- ✅ LLM Client
- ✅ Conversation Memory

但是，它仍然只能依赖模型已有知识。

下一章将实现 **Tool（工具）**。

让 Agent 学会调用外部工具，而不仅仅依赖大模型本身。