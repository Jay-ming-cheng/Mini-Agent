
from llm.client import LLMClient
from tools.calculator import Calculator
import json
from memory.memory import Memory

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
        self.memory = Memory()

        self.tools = {
            "calculator": Calculator()
        }



    def chat(self,message:str) -> str:
        observations = []
        reflection = None
        memory = self.memory.get_all()

        MAX_STEPS = 10
        for step in range(MAX_STEPS):
            action = self._reason(
                message,
                observations,
                reflection,
                memory
            )
            if action["type"] == "finish":

                memory = self._extract_memory(message)

                if memory["save"]:
                    self.memory.save(
                        memory["key"],
                        memory["value"]
                    )


                return action["answer"]
            elif action["type"] == "action":


                observation = self._execute_action(action)
                observations.append(observation)

                reflection = self._reflect(
                    message,
                    observation
                )
            else:
                raise ValueError(
                    f"Unknown action type: {action['type']}"
                )



    def _build_prompt(
            self,
            message: str,
            observations: list[dict],
            reflection,
            memory
    ) -> str:
        memory_text = ""
        if not memory:
            memory_text = "Memory:\nNone"
        for key, value in memory.items():
            memory_text += f"{key}: {value}\n"
        observation_text = ""
        if not observations:
            observation_text = "Observation:\nNone"

        for i, observation in enumerate(observations, start=1):
            observation_text += (
                f"Observation {i}\n"
                f"Tool: {observation['tool']}\n"
                f"Result: {observation['result']}\n\n"
            )

        if reflection is None:
            reflection_text = "Reflection:\nNone"
        else:
            reflection_text = f"""
        Reflection:

        Status:
        {reflection["status"]}

        Reason:
        {reflection["reason"]}
        """

        prompt = f"""
        你是一个 Agent。

        你的职责：

        1. 根据当前信息决定下一步行动。
        2. 可以调用 Tool。
        3. 如果任务已经完成，则直接返回最终答案。
        4. 对于所有数学计算任务，
        必须先调用 calculator。
        
        5. 即使数学表达式存在错误，
        也必须先调用 calculator 获取 Tool 返回结果。
        
        6. 不允许自己计算，也不允许自己判断表达式是否合法。

        当前可用 Tool：

        1. calculator
           用于计算数学表达式。
           
           
        Memory:

        {memory_text}

        Observations

        {observation_text}  
        
        {reflection_text}

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
            observations: list[dict],
            reflection: dict | None,
            memory: dict
    ) -> dict:

        prompt = self._build_prompt(message,observations,reflection,memory)
        action = self.llm.chat(prompt,save_history=False)
        action = json.loads(action)
        return action



    def _execute_action(self,action: dict) -> dict:
        tool_name = action["tool"]
        tool_input = action["input"]
        tool = self.tools.get(tool_name)
        if tool is None:
            raise ValueError(f"Tool '{tool_name}' not found.")
        try:
            result = tool.run(tool_input)

        except Exception as e:
            result = str(e)

        observation = {
            "tool": tool_name,
            "result": result
        }

        return observation



    def _reflect(self,
                 message: str,
                 observation: dict) -> dict:
        """
        根据 Observation 判断上一轮执行情况。
        """
        prompt = f"""
        你是一个 Reflection Agent。

        你的职责：

        根据 Tool 返回结果，判断这次执行是否成功。

        用户问题：

        {message}

        Tool：

        {observation["tool"]}

        Tool 返回：

        {observation["result"]}

        如果执行成功，请返回：

        {{
            "status":"success",
            "reason":"..."
        }}

        如果执行失败，请返回：

        {{
            "status":"failure",
            "reason":"..."
        }}

        不要输出 Markdown。

        不要解释。

        只输出 JSON。
        """
        result = self.llm.chat(
            prompt,
            save_history=False
        )

        reflection = json.loads(result)

        return reflection

    def _extract_memory(
            self,
            message: str
    ) -> dict:
        prompt = f"""
        你是一个 Memory Extractor。

        你的职责：
        
        判断用户输入中是否包含值得长期保存的信息。
        
        例如：
        
        姓名
        
        年龄
        
        职业
        
        城市
        
        兴趣
        
        偏好
        
        用户输入：

        {message}
        
        
        如果没有需要保存的信息，请返回：
        
        {{
            "save": false
        }}
        
        如果有，请返回：
        
        {{
            "save": true,
            "key":"name",
            "value":"Jay"
        }}
        
        不要输出 Markdown。
        
        不要解释。
        
        只输出 JSON。
        """
        result = self.llm.chat(
            prompt,
            save_history=False
        )

        memory = json.loads(result)

        return memory