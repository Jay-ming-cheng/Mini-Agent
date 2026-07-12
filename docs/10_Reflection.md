# Reflection

> Reflection Workflow

---

# 为什么需要 Reflection？

完成 ReAct 之后，Agent 已经可以：

```
Reason
    ↓
Action
    ↓
Observation
```

但是还存在一个问题：

Agent 只能看到 Tool 返回的结果，却不会主动分析：

- Tool 是否执行成功？
- Tool 是否执行失败？
- 是否应该继续执行？
- 是否应该直接结束？

因此，需要新增一个 Reflection（反思）模块。

Reflection 的职责不是调用 Tool，而是分析 Observation，并将分析结果反馈给下一轮 Reason。

---

# Reflection 的职责

Reflection 负责：

- 分析 Tool 返回结果
- 判断执行是否成功
- 给出执行原因
- 为下一轮推理提供参考

它不会：

- 调用 Tool
- 修改 Observation
- 输出最终答案

因此 Reflection 更像是一个中间分析器。

---

# Workflow

加入 Reflection 后，整个 Agent Workflow 变成：

```
User
    ↓
Reason
    ↓
Action
    ↓
Tool
    ↓
Observation
    ↓
Reflection
    ↓
Reason
    ↓
Finish
```

相比 ReAct，多了一次执行后的分析过程。

---

# Reflection Prompt

Reflection 同样由 LLM 完成。

Prompt 的目标只有一个：

根据 Observation 判断 Tool 是否执行成功。

例如：

```
Tool：

calculator

Tool Result：

非法数学表达式：12/*
```

LLM 返回：

```json
{
    "status": "failure",
    "reason": "Tool 返回错误，数学表达式非法。"
}
```

如果 Tool 正常执行：

```json
{
    "status": "success",
    "reason": "Tool 执行成功，可以继续完成回答。"
}
```

Reflection 输出统一采用 JSON，方便 Agent 后续解析。

---

# 为什么不用 Tool 自己判断？

一种方案是：

Tool 自己返回：

```python
{
    "status": "success"
}
```

但是这种设计存在问题。

每个 Tool 都需要维护自己的状态判断逻辑。

例如：

Calculator：

```
success
failure
```

Search：

```
timeout
success
not found
```

SQL：

```
permission denied
syntax error
success
```

不同 Tool 的返回格式会越来越复杂。

因此选择：

Tool 只负责执行。

Reflection 负责分析。

职责更加清晰。

---

# Observation 与 Reflection

Observation：

表示 Tool 的执行结果。

例如：

```python
{
    "tool": "calculator",
    "result": "非法数学表达式：12/*"
}
```

Reflection：

表示 Agent 对 Observation 的分析。

例如：

```python
{
    "status": "failure",
    "reason": "数学表达式非法。"
}
```

两者职责不同：

Observation 是事实。

Reflection 是分析。

---

# Agent Workflow

Agent 每轮循环：

```
Reason

↓

Action

↓

Execute Tool

↓

Observation

↓

Reflection

↓

Next Reason
```

下一轮 Reason 会同时看到：

- 用户问题
- Observation
- Reflection

因此能够根据上一轮执行情况决定：

- 是否继续调用 Tool
- 是否结束任务

---

# 异常处理

Tool 执行过程中可能出现异常。

例如：

```
12/*
```

Calculator 会抛出异常。

如果直接终止程序：

```
Tool Exception

↓

Program Exit
```

整个 Agent 会停止运行。

因此改为：

```
Tool Exception

↓

Observation

↓

Reflection

↓

Reason
```

即使 Tool 执行失败，Agent 仍然能够继续完成整个 Workflow。

---

# 本模块完成内容

✅ 新增 `_reflect()`

✅ Reflection Prompt

✅ Reflection JSON 输出

✅ Observation 分析

✅ Reflection 接入 ReAct Loop

✅ Tool 异常进入 Observation

✅ 下一轮 Reason 使用 Reflection

---

# 学到的内容

Reflection 并不是重新思考整个问题。

它只负责分析：

> 刚刚执行得怎么样？

真正的推理由 Reason 完成。

Reflection 的作用是：

**让 Agent 能够利用上一轮执行结果，对下一轮决策提供参考。**

这也是现代 Agent Workflow 中常见的设计模式之一。