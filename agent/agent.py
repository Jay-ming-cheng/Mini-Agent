
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



    def _plan(self,message: str) -> list[dict]:
        """
        根据用户输入生成执行计划。

        Args:
            message: 用户输入。

        Returns:
            Plan（步骤列表）。
        """
        prompt = f"""
        你是一个 Planner。

        你的职责是根据用户输入生成执行计划。
        
        请只返回 JSON 数组。
        
        每一步包含：
        
        - step
        - tool
        - input
        
        如果无需 Tool：
        
        返回：
        []
        
        当前可用 Tool：
        calculator：用于数学表达式计算。
        
        例如：
        用户：
        计算 (23+99)*8
        返回：
        [
            {{
                "step":1,
                "tool":"calculator",
                "input":"(23+99)*8"
            }}
        ]

        用户输入：
        
        {message}
        """
        result = self.llm.chat(
            prompt,
            save_history=False
        )
        plan = json.loads(result)
        return plan


    def chat(self,message:str) -> str:
        """
           与 Agent 进行一次对话。

           Args:
               message: 用户输入。

           Returns:
               Agent 回复内容。
        """

        plan = self._plan(message)

        if plan == []:
            return self.llm.chat(message)

        step = plan[0]

        tool = self.tools.get(step["tool"])

        if tool is None:
            raise ValueError(
                f"Tool '{step['tool']}' not found."
            )

        try:
            tool_result = tool.run(step["input"])
        except Exception as e:
            return f"Tool 执行失败：{e}"

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