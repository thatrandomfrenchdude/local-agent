import asyncio

from src.agent import Agent
from src.tools import tools, tool_descriptions

def main():
    instructions = (
        "You are a tool-calling agent that may use the following tools by responding according to their instructions.\n"
        "Available tools:\n"
        f"{tool_descriptions}\n"
        "If no tool is needed, respond with the final answer."
    )

    agent = Agent(
        tools=tools,
        instructions=instructions
    )

    print("Type 'exit' or 'quit' to end the chat.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        result = asyncio.run(agent.run(user_input))
        print(f"Agent: {result}")

if __name__ == "__main__":
    main()