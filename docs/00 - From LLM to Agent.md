# 00 - From LLM to Agent

## 为什么会做这个项目？

学习大语言模型的过程中，我发现很多 Agent 框架已经非常成熟。

例如：

- LangChain
- LangGraph
- AutoGen
- CrewAI

使用这些框架，只需要几行代码就可以快速构建一个 Agent。

但是随着学习的深入，我逐渐意识到一个问题：

> 会使用框架，并不代表真正理解 Agent。

很多时候，一个 Agent 只需要：

```python
agent.run(...)
```

就能够完成复杂任务。

但如果不知道内部发生了什么，就很难理解：

- 为什么需要 Planning？
- 为什么需要 Tool？
- 为什么需要 Reflection？
- 为什么 Memory 不等于 Conversation History？
- 一个 Agent 为什么能够不断完成复杂任务？

因此，我决定从零开始，不依赖任何 Agent 框架，实现一个属于自己的 Mini Agent。

整个项目只有一个目标：

> 理解 Agent Workflow。

---

# 我理解的 Agent

项目开始之前，我认为：

> Agent 就是一个能够调用 Tool 的 LLM。

项目完成之后，我对 Agent 的理解发生了变化。

现在我认为：

> Agent 并不是某一个模型，而是一套 Workflow。

LLM 只是其中负责推理（Reason）的一个模块。

真正决定 Agent 能力的，是 Workflow 如何组织。

---

# Mini Agent 的演进过程

整个项目按照由浅入深的方式逐步完成。

## Step 1：LLM

最开始，项目只有：

```python
llm.chat(...)
```

LLM 能回答问题。

但只能依赖 Prompt。

---

## Step 2：Conversation History

加入 Conversation History 后，

模型终于能够进行连续对话。

例如：

```text
我叫 Jay。

↓

我叫什么？
```

但是：

Conversation History 会越来越长。

它并不能解决长期记忆的问题。

---

## Step 3：Tool

LLM 本身不能完成所有任务。

例如：

- 数学计算
- 文件读取
- 网络请求

因此引入 Tool。

LLM 不再直接解决问题，

而是决定：

> 是否调用 Tool。

---

## Step 4：Agent

Agent 成为了整个系统的统一入口。

它负责：

- 接收用户请求
- 调用 LLM
- 调用 Tool
- 协调整个 Workflow

Agent 本身并不负责完成所有工作。

它更像一个协调者。

---

## Step 5：Planning

复杂任务并不能一次完成。

因此需要：

Planning。

LLM 首先生成执行计划。

然后再一步一步执行。

Planning 负责：

> 决定做什么。

---

## Step 6：ReAct

Planning 解决了：

做什么。

但是：

每完成一步之后，

Agent 都需要重新思考。

于是加入：

ReAct。

整个 Workflow 变成：

```text
Reason

↓

Action

↓

Observation

↓

Reason
```

Agent 开始能够根据新的信息不断调整自己的行为。

---

## Step 7：Reflection

即使 Tool 已经执行完成，

也不能保证执行成功。

因此：

Reflection 负责分析：

这一步到底成功了吗？

Reflection 并不会直接解决问题。

它只是给下一轮 Reason 提供反馈。

Workflow 进一步变成：

```text
Reason

↓

Action

↓

Observation

↓

Reflection

↓

Reason
```

---

## Step 8：Memory

Memory 是整个项目最后完成的模块。

也是我理解变化最大的地方。

最开始，

我认为：

Conversation History 就是 Memory。

后来发现：

两者完全不同。

Conversation History：

保存聊天记录。

Memory：

保存长期知识。

例如：

```text
姓名

城市

兴趣

职业
```

Memory Workflow 包括：

```text
Retrieve

↓

Store
```

用户新的输入，

不仅用于回答问题，

还可能更新长期 Memory。

---

# 我最大的收获

完成整个项目后，

我最大的收获并不是代码。

而是理解了 Agent 的设计思想。

我逐渐意识到：

现代 Agent 并不是：

> 一个更强大的模型。

而是：

> 多个模块共同组成的一套 Workflow。

LLM 负责推理。

Tool 负责执行。

Planning 负责规划。

Reflection 负责反馈。

Memory 负责长期知识。

这些模块共同组成了一个真正能够持续完成任务的 Agent。

---

# 对 Prompt Engineering 的理解

项目开始之前，

我认为 Prompt Engineering 是：

> 写一句更好的 Prompt。

完成整个项目之后，

我认为：

Prompt Engineering 更像是在设计：

> LLM 与各个模块之间的通信协议。

例如：

- Reason Prompt
- Reflection Prompt
- Memory Prompt

它们的职责完全不同。

Prompt 不只是提问，

更是在组织整个 Workflow。

---

# 对未来学习路线的思考

完成 Mini Agent v1.0 后，

我认为自己已经理解了 Agent 的基础 Workflow。

下一步，我希望继续学习：

- Agentic RAG
- MCP（Model Context Protocol）
- Multi-Agent
- Enterprise AI Agent

进一步理解企业级 Agent 系统的设计与实现。

---

# 最后

整个 Mini Agent 项目并不是为了实现一个功能完整的 Agent。

而是希望通过不断拆解 Agent 的每一个模块，

真正理解：

> 一个现代 AI Agent 为什么能够工作。

相比直接使用框架，

我更希望知道：

每一个 Workflow 为什么存在。

只有理解了这些设计思想，

未来学习任何 Agent 框架，

都会更加容易。