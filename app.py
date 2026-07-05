from config import Config
from llm.client import LLMClient


llm = LLMClient()

response = llm.chat("我的名字叫JAY")

print(response)

print(llm.chat("我叫什么？"))


# if __name__ == "__main__":
#     main()