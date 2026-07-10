
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



    def chat(self,message:str) -> str:
        observations = []

        MAX_STEPS = 10
        for step in range(MAX_STEPS):
            action = self._reason(
                message,
                observations
            )
            if action["type"] == "finish":
                return action["answer"]
            elif action["type"] == "action":
                observation = self._execute_action(action)
                observations.append(observation)
            else:
                raise ValueError(
                    f"Unknown action type: {action['type']}"
                )



    def _build_prompt(
            self,
            message: str,
            observations: list[dict]
    ) -> str:
        observation_text = ""
        if not observations:
            observation_text = "Observation:\nNone"

        for i, observation in enumerate(observations, start=1):
            observation_text += (
                f"Observation {i}\n"
                f"Tool: {observation['tool']}\n"
                f"Result: {observation['result']}\n\n"
            )

        prompt = f"""
        你是一个 Agent。

        你的职责：

        1. 根据当前信息决定下一步行动。
        2. 可以调用 Tool。
        3. 如果任务已经完成，则直接返回最终答案。

        当前可用 Tool：

        1. calculator
           用于计算数学表达式。

        Observations

        {observation_text}  

        用户输入:

        {message}

        Action:

        {{
            "type":"action",
            "tool":"calculator",
            "input":"..."
        }}

       Finish:

        {{
            "type":"finish",
            "answer":"..."
        }}

        不要输出 Markdown。

        不要输出解释。

        只输出 JSON。
       """
        return prompt



    def _reason(
            self,
            message: str,
            observations: list[dict]
    ) -> dict:

        prompt = self._build_prompt(message,observations)
        action = self.llm.chat(prompt,save_history=False)
        action = json.loads(action)
        return action





        


    def _execute_action(self,action: dict) -> dict:
        tool_name = action["tool"]
        tool_input = action["input"]
        tool = self.tools.get(tool_name)
        if tool is None:
            raise ValueError(f"Tool '{tool_name}' not found.")
        observation = {
            "tool": tool_name,
            "result": tool.run(tool_input)
        }
        return observation

