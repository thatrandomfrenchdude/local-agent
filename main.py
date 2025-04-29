import asyncio

from src.agent import Agent
from src.model import chat_completion
from src.tools import tools, Tool, tool_descriptions

# --- USER CONFIGURATION ---
# Set the model you want to use
MODEL = "DeepSeek-R1-Distill-Llama-8B-GGUF/DeepSeek-R1-Distill-Llama-8B-Q8_0.gguf"

def main():
    # Instructions for the agent, including tool references
    instructions = (
        "You are an agent that may call tools by responding with TOOL_NAME(argument).\n"
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

    # Run the agent with some user input (normal output)
    result = asyncio.run(agent.run("Please echo ‘hello world’."))
    print("Agent result:", result)

    # # Example: Run the agent with streaming output
    # asyncio.run(agent.run("What time is it?", stream=True))

if __name__ == "__main__":
    main()