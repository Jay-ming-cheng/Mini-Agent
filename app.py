from llm.client import LLMClient
from agent.agent import Agent

llm = LLMClient()
agent = Agent(llm)

while True:
    message = input("You: ")

    if message.lower() == "exit":
        break

    print("Agent:", agent.chat(message))