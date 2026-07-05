# Tool

## 1. 什么是 Tool？

Tool 是 Agent 获得外部能力的方式。

LLM 本身只能生成文本，并不能真正访问外部世界。

例如：

- 查询天气
- 打开浏览器
- 操作 Excel
- 搜索网络
- 计算数学表达式

这些能力都需要通过 Tool 实现。

---

## 2. 为什么需要 Tool？

LLM 的知识来自训练数据。

它不知道：

- 实时天气
- 当前时间
- 本地文件
- 数据库内容

因此，Agent 需要借助 Tool 与真实世界交互。

---

## 3. Tool 的职责

Tool 只负责完成一项具体功能。

例如：

Calculator：

输入：

2 + 3

输出：

5

它不知道：

- 谁调用了它
- 为什么调用
- 最终结果如何展示

---

## 4. 为什么 Tool 不负责组织语言？

Tool 返回的是数据（Data）。

例如：

```python
return 5
```

而不是：

```text
计算结果是 5。
```

组织自然语言属于 LLM 的职责。

保持职责单一，可以降低模块之间的耦合。

---

## 5. 为什么 Tool 不直接调用 LLM？

Tool 是整个系统中的底层能力模块。

它不应该知道：

- LLM
- Agent
- Memory
- Planning

否则 Tool 将与整个系统高度耦合。

---

## 6. Tool 的 Workflow

User

↓

Agent

↓

LLM 判断是否需要 Tool

↓

Agent 调用 Tool

↓

Tool 返回数据

↓

LLM 组织自然语言

↓

User

---

## 7. 当前实现

当前实现了第一个 Tool：

Calculator

接口：

```python
calculate(expression: str) -> int | float
```

功能：

- 接收数学表达式
- 返回计算结果
- 非法表达式抛出异常

---

## 8. 为什么使用 eval()？

当前使用 eval() 仅用于演示 Tool Workflow。

真实项目中，不应直接执行用户输入。

应使用安全的表达式解析器替代 eval()。