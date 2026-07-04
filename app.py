from config import Config
from llm.client import LLMClient


llm = LLMClient()

response = llm.chat("请用一句话介绍你自己.")

print(response)


# if __name__ == "__main__":
#     main()