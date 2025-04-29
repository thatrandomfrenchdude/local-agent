import asyncio

from src.agent import Agent
from src.tools import tools, tool_descriptions

# Set the model you want to use
MODEL = "hugging-quants/llama-3.2-3b-instruct"

def main():
    instructions = (
        "You are a tool-calling agent that may use the following tools by responding according to their instructions.\n"
        "Available tools:\n"
        f"{tool_descriptions}\n"
        "If no tool is needed, respond with the final answer."
    )
    # Create the agent
    agent = Agent(
        model=MODEL,
        tools=tools,
        instructions=instructions
    )

    # # Run the agent with some user input (normal output)
    # result = asyncio.run(agent.run("Please echo ‘hello world’."))

    # Example: Run the agent with streaming output
    result = asyncio.run(agent.run("What time is it?"))

    print("Agent result:", result)

if __name__ == "__main__":
    main()