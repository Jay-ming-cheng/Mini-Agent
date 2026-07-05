from llm.client import LLMClient


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
    def chat(self,message:str) -> str:
        """
           与 Agent 进行一次对话。

           Args:
               message: 用户输入。

           Returns:
               Agent 回复内容。
        """
        return self.llm.chat(message)