from json import tool
from unittest import result

from llm.client import LLMClient
from tools.calculator import Calculator
import json

class Agent:
    """
    Agent.

    职责：
    1. 作为整个系统的统一入口。
    2. 接收用户请求。
    3. 协调各个模块完成任务。

    注意：
    - 不负责与模型底层通信（LLMClient 负责）。
    - 不负责实现 Tool（Tool 模块负责）。
    - 不负责管理长期 Memory（后续版本实现）。
    """
    def __init__(self,llm: LLMClient):
        """
           初始化 Agent。

           Args:
               llm: 已创建好的 LLMClient 实例。
        """
        self.llm = llm

        self.tools = {
            "calculator": Calculator()
        }

    def _decide_tool(self,message: str):
        """
        让 LLM 判断是否需要调用 Tool。
        """
        prompt = f"""
        你是一个 Agent。

        你的任务是判断用户是否需要调用 Tool。

        当前可用 Tool：

        1. calculator
           用于数学表达式计算。

        如果需要调用 Tool。

        请严格输出如下 JSON：

        {{
            "tool":"calculator",
            "expression":"数学表达式"
        }}

        如果不需要调用 Tool。

        请只输出：

        NONE

        用户输入：

        {message}
        """
        result = self.llm.chat(prompt,save_history=False)
        if result == "NONE":
            return None
        else:
            return json.loads(result)

    def chat(self,message:str) -> str:
        """
           与 Agent 进行一次对话。

           Args:
               message: 用户输入。

           Returns:
               Agent 回复内容。
        """

        decision = self._decide_tool(message)

        if decision is None:
            return self.llm.chat(message)

        tool = self.tools.get(decision["tool"])

        if tool is None:
            raise ValueError(f"Tool{decision['tool']} not found.")

        tool_result = tool.run(decision["expression"])

        return self._generate_response(message,tool_result)

    def _generate_response(self,message: str,tool_result: str) -> str:
        """
        根据 Tool 返回结果生成最终回复。
        """
        prompt = f"""
        你是一个 AI 助手。

        用户的问题：
        {message}

        Tool 返回结果：
        {tool_result}

        请根据 Tool 返回结果回答用户。

        要求：
        1. 不要重新计算。
        2. 不要修改 Tool 返回结果。
        3. 不要编造 Tool 没有提供的信息。
        4. 使用自然、友好的语言回答。
        """
        return self.llm.chat(prompt,save_history=False)