# Step 8：Planning

## 为什么需要 Planning？

在上一章节中，Agent 已经能够完成 Tool Calling。

Workflow 如下：

User
↓

LLM（判断是否调用 Tool）
↓

Tool
↓

LLM（组织回答）
↓

User

这种方式可以完成简单任务，例如：

- 计算数学表达式
- 查询天气（未来）
- 调用单个 Tool

但是，当用户提出复杂任务时，仅依靠一次 Tool Calling 已无法完成。

例如：

> 先计算 (23+99)，再乘以 8，最后告诉我结果是否小于 1000。

这种任务需要：

- 拆解任务
- 规划执行步骤
- 顺序执行多个 Tool

因此，需要引入 Planning。

---

## 什么是 Planning？

Planning 的职责是：

**将自然语言任务拆解为多个可执行步骤。**

例如：

用户输入：

先计算 (23+99)，再乘以 8。

Planner 输出：

```json
[
    {
        "step":1,
        "tool":"calculator",
        "input":"23+99"
    },
    {
        "step":2,
        "tool":"calculator",
        "input":"122*8"
    }
]
```

Agent 不再决定是否调用 Tool。

而是执行 Planner 生成的 Plan。

---

## 为什么使用 Plan，而不是 Tool Decision？

之前：

Decision：

```json
{
    "tool":"calculator",
    "expression":"23+99"
}
```

只能支持一次 Tool 调用。

Planning：

```json
[
    {
        "step":1,
        "tool":"calculator",
        "input":"23+99"
    }
]
```

虽然目前只有一步。

但未来可以扩展为：

```json
[
    {...},
    {...},
    {...}
]
```

因此：

**Decision 可以看作只有一步的 Planning。**

Planning 的抽象能力更强，也更容易扩展。

---

## Planning Workflow

Planning 引入后，Agent Workflow 更新为：

User

↓

Planner（LLM）

↓

Plan

↓

Agent

↓

Tool

↓

LLM（生成最终回复）

↓

User

相比之前：

Agent 不再关心：

- 是否调用 Tool

而是：

- 获取 Plan
- 执行 Plan

职责更加单一。

---

## 为什么 Planning 不保存聊天历史？

Planning 属于 Agent 的内部思考过程。

这些 Prompt 不属于用户对话。

如果保存到聊天历史：

- 会污染 Conversation Memory
- 增加 Token 消耗
- 影响后续聊天

因此：

Planner 使用：

```python
save_history=False
```

---

## 当前版本限制（Planning V1）

目前 Planning 仅支持：

- 一个 Tool
- 一个执行步骤

虽然 Plan 使用 List 表示。

但 Agent 当前仅执行：

```python
step = plan[0]
```

这样设计的原因是：

目前尚未实现：

- Observation
- ReAct
- Reflection

因此：

暂不支持真正的多步执行。

---

## 下一步

Planning V2 将升级为真正的 Agent Workflow：

Think

↓

Plan

↓

Act

↓

Observe

↓

Repeat

Agent 将能够：

- 顺序执行多个 Tool
- 根据 Tool 输出继续规划
- 完成复杂任务