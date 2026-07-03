## 1.为什么需要 LLM Client？
Planner Reflection Memory Agent等等这些都需要llm ，难道每次用的时候都client = OpenAI(...)吗？
肯定不啊，所以应该把**LLM 应该成为整个项目最底层的服务**。

## 2.为什么不能直接 OpenAI()
如果整个项目到处都是：client = openAi()
例如：
每个模块都会重复创建 Client。
API Key 和 Base URL 分散在各个文件中。
修改配置需要同时修改很多地方。
每个模块都直接依赖 OpenAI SDK，耦合度非常高。

这意味着，只要底层 SDK 或 Provider 发生变化，上层所有模块都需要修改。
这种设计在软件工程中被称为 **高耦合（High Coupling）**。
## 3.为什么要封装？
因为如果以后
API Key 换了
Model 换了
OpenAI 换成 DeepSeek
DeepSeek 换成 Qwen；整个项目都要一个一个改。而我只希望整个项目只知道LLMClient，至于底层是谁就可以不用知道唠。
**依赖抽象，而不是依赖具体实现。**
## 4.为什么 Agent 不应该依赖 SDK？
Agent 的职责应该是：
理解任务
做出决策
调用工具
组织 Workflow
而不是：

创建 HTTP Client
管理 API Key
拼接请求参数
调用第三方 SDK

如果 Agent 直接负责这些工作，它就同时承担了：

业务逻辑
网络通信
配置管理

这违反了软件工程中的**单一职责原则（Single Responsibility Principle）**。

因此，我们把与大模型通信相关的所有逻辑，都交给 LLMClient。
## 5.以后怎样扩展？
目前第一版 LLMClient 只支持：

输入一句话

↓

返回一句回答

接口非常简单：

llm.chat(message: str)

随着 Mini Agent 的不断完善，我们会逐步扩展它的能力，而不是一次性实现所有功能。

例如：

Step 1：单轮对话（当前）
llm.chat(message)
Step 2：多轮对话

支持 Message History：

llm.chat(messages)

为 Memory 做准备。

Step 3：System Prompt

支持：

system_prompt

方便 Planner、Reflection 使用不同角色。

Step 4：Tool Calling

支持模型调用工具（Function Calling）。

为 Agent 增加执行能力。

Step 5：Streaming

支持流式输出，提高用户体验。

Step 6：Structured Output

支持 JSON 输出。

方便 Reflection、Planning 等 Workflow 解析结果。

整个演进路线如下：

Single Chat
        │
        ▼
Message History
        │
        ▼
System Prompt
        │
        ▼
Tool Calling
        │
        ▼
Streaming
        │
        ▼
Structured Output

我们不会一次性实现所有能力，而是遵循整个 Mini Agent 的开发原则：

**一次只增加一种能力**。

这样可以更清楚地观察每一种 Workflow 对 Agent 行为带来的影响。