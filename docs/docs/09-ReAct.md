# 09 - ReAct Workflow

---

# 为什么需要 ReAct？

在上一章节中，我们已经实现了 Planning Workflow。

Planning 的思想是：

> **先规划（Plan），再执行（Execute）。**

例如：

用户输入：

```text
计算 (23+99)*8
```

Planner 会首先生成完整的执行计划：

```json
[
    {
        "step": 1,
        "tool": "calculator",
        "input": "(23+99)*8"
    }
]
```

随后 Agent 根据 Plan 执行 Tool，并返回最终结果。

这种方式已经能够完成许多简单任务，但随着任务变得复杂，Planning 开始暴露一些问题。

---

# Planning 的局限性

Planning 最大的特点是：

**所有步骤都会在执行之前一次性生成。**

例如：

```text
Step 1
↓

Step 2
↓

Step 3
```

如果：

- Step1 调用 Tool 失败
- Tool 返回了意料之外的结果
- 用户环境发生变化

那么：

后面的 Step2、Step3 很可能已经不再正确。

也就是说：

Planning **不能根据执行结果动态调整下一步行为。**

这也是现代 Agent 为什么开始大量采用 ReAct Workflow 的原因。

---

# 什么是 ReAct？

ReAct（Reason + Act）是一种经典的 Agent Workflow。

它的核心思想不是：

> **先规划所有步骤。**

而是：

> **边思考（Reason），边行动（Action），再根据行动结果继续思考。**

整个过程不断循环，直到任务完成。

Workflow 如下：

```text
Reason
    ↓
Action
    ↓
Observation
    ↓
Reason
```

因此，ReAct 比 Planning 更加灵活，也更加适合真实世界中的复杂任务。

---

# ReAct Workflow

本项目中的 ReAct Workflow 如下：

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

整个 Agent 会不断重复：

Reason → Action → Observation

直到模型认为任务已经完成。

---

# Reason

Reason 是整个 ReAct Workflow 的核心。

在本项目中，由 `_reason()` 负责。

它的职责只有一个：

> **根据当前信息决定下一步应该做什么。**

Reason 不负责：

- 调用 Tool
- 计算结果
- 返回最终回复

Reason 只负责思考。

例如：

```json
{
    "type": "action",
    "tool": "calculator",
    "input": "(23+99)*8"
}
```

或者：

```json
{
    "type": "finish",
    "answer": "计算结果是 976。"
}
```

因此：

Reason 更像整个 Agent 的"大脑"。

---

# Action

Action 由 `_execute_action()` 完成。

它的职责非常简单：

1. 找到对应 Tool
2. 调用 Tool
3. 返回执行结果

例如：

```python
tool = self.tools.get(tool_name)

result = tool.run(tool_input)
```

Action **绝不会再次调用 LLM。**

因为：

Reason 与 Action 应该保持职责分离（Single Responsibility Principle）。

---

# Observation

Tool 执行完成以后，并不会直接结束。

Tool 的返回结果会被保存为：

```python
{
    "tool": "calculator",
    "result": 976
}
```

这就是 Observation。

Observation 的作用是：

> **告诉下一轮 Reason：刚刚发生了什么。**

所有 Observation 会保存在：

```python
observations = []
```

例如：

```python
[
    {
        "tool": "calculator",
        "result": 976
    }
]
```

下一轮 Prompt 会把这些 Observation 一起发送给 LLM。

因此：

LLM 可以根据最新的执行结果继续思考。

---

# ReAct Loop

整个 Agent 的核心循环如下：

```python
for _ in range(MAX_STEPS):

    action = self._reason(...)

    if action["type"] == "finish":
        return action["answer"]

    observation = self._execute_action(action)

    observations.append(observation)
```

整个流程不断重复：

```text
Reason

↓

Action

↓

Observation

↓

Reason
```

直到：

```json
{
    "type":"finish"
}
```

Agent 才结束任务。

为了避免死循环，本项目加入：

```python
MAX_STEPS = 10
```

当循环超过最大次数时：

```python
raise RuntimeError(...)
```

主动终止程序。

---

# 为什么这样设计？

本项目将 ReAct 拆分为了三个函数：

```text
_reason()

_execute_action()

chat()
```

每个函数都只有一个职责。

## _reason()

负责：

- 构造 Prompt
- 调用 LLM
- 返回 Action

不负责：

- Tool
- Observation

---

## _execute_action()

负责：

- 调用 Tool
- 返回 Observation

不负责：

- Prompt
- LLM

---

## chat()

负责：

- 控制整个 Workflow
- 保存 Observation
- 控制 Loop

不负责：

- 推理
- Tool 执行

这种设计符合：

> **Single Responsibility Principle（单一职责原则）**

模块之间更加独立，也更容易扩展。

---

# 本次重构内容

相比 Planning Workflow，本次新增：

- `_build_prompt()`
- `_reason()`
- `_execute_action()`
- Observation
- ReAct Loop

同时：

Agent 不再一次性执行整个 Plan。

而是在每一步执行之后重新进行 Reason。

---

# 学到了什么？

在实现 ReAct 的过程中，我最大的收获并不是学会了新的 Prompt。

真正重要的是理解了：

> **Workflow 比 Prompt 更重要。**

Planning：

> 先规划，再执行。

ReAct：

> 边思考，边执行，边观察，再继续思考。

两者最大的区别不是 Prompt，而是整个 Agent 的工作方式。

另外，我也第一次真正理解了：

- Observation 为什么存在
- 为什么需要 Loop
- 为什么要拆分 Reason 与 Action
- 为什么 Agent 要遵循单一职责原则

相比第一版只能简单调用 Tool 的 Agent，现在已经实现了一个具备：

- Reason
- Action
- Observation
- Loop

四个核心能力的 ReAct Agent。

这也为后续实现 Reflection、Memory 等更高级 Workflow 奠定了基础。