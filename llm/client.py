from openai import OpenAI
from config import Config

class LLMClient:
    """
    LLM 客户端。

    职责：
    1. 负责与大模型通信。
    2. 屏蔽不同模型 SDK 的差异。
    3. 向上层提供统一的调用接口。

    注意：
    - 不负责 Planning。
    - 不负责 Reflection。
    - 不负责 Tool 调度。
    - 不负责 Memory 管理。
    """
    def __init__(self):
        """
        初始化 LLM 客户端。

        在创建对象时初始化 OpenAI Client，
        避免每次调用 chat() 时重复创建。
        """
        # 创建与大模型通信的客户端，整个生命周期只创建一次
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY,base_url=Config.OPENAI_BASE_URL)
        # 保存当前使用的模型名称
        self.model = Config.MODEL_NAME
        # 保存当前会话的聊天记录
        self.messages = []



    def chat(self, message: str) -> str:
        """
        与大模型进行一次对话。

        Args:
            message: 用户输入的问题。

        Returns:
            大模型回复的文本内容。
        """
        self.messages.append(
            {
                "role":"user",
                "content":message

            }
        )



        response = self.client.chat.completions.create(model=self.model,messages=self.messages)
        assistant_message = response.choices[0].message.content
        self.messages.append(
            {
                "role":"assistant",
                "content":assistant_message
            }
        )
        return assistant_message

