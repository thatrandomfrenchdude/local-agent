import asyncio
from typing import List, Dict, Callable, Any
from openai import OpenAI
from datetime import datetime

# --- LM Studio Client Setup ---
LM_STUDIO_URL = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
client = OpenAI(base_url=LM_STUDIO_URL, api_key=LM_STUDIO_API_KEY)

# A message is a dictionary with a role and content
Message = Dict[str, str]

def chat_completion(
    model: str,
    messages: List[Message],
    temperature: float = 0.7,
    stream: bool = False
) -> Any:
    """Send messages to the language model and get a response."""
    if stream:
        # For streaming responses (returns an async generator)
        return client.chat.completions.acreate(
            model=model, messages=messages,
            temperature=temperature, stream=True
        )
    # For normal responses
    resp = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature
    )
    return resp.choices[0].message.content

async def stream_chat(
    model: str,
    messages: List[Message],
    temperature: float = 0.7
) -> None:
    """Stream tokens from LM Studio and print them live."""
    stream = await chat_completion(model, messages, temperature, stream=True)
    async for chunk in stream:
        # Each chunk may contain a piece of the response
        delta = chunk.choices[0].delta.get("content", "")
        if delta:
            print(delta, end="", flush=True)
    print()  # Newline at the end

# --- Tool Abstraction ---
class Tool:
    def __init__(self, name: str, func: Callable[[str], str], description: str):
        self.name = name
        self.func = func
        self.description = description

    def run(self, arg: str) -> str:
        return self.func(arg)

# --- Agent Class ---
class Agent:
    def __init__(
        self,
        model: str,
        tools: List[Tool],
        instructions: str,
        max_turns: int = 5
    ):
        self.model = model
        self.tools = {tool.name: tool for tool in tools}
        self.instructions = instructions
        self.max_turns = max_turns

    async def run(self, user_input: str, stream: bool = False) -> str:
        """Talk to the model and use tools if needed. Streams only the final response if requested."""
        history: List[Message] = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": user_input}
        ]

        final_response = None
        for _ in range(self.max_turns):
            response = chat_completion(self.model, history, stream=False)
            if "(" in response and response.endswith(")"):
                name, arg = response.split("(", 1)
                arg = arg.rstrip(")")
                tool = self.tools.get(name.strip())
                if tool:
                    result = tool.run(arg)
                    history.append({"role": "assistant", "content": response})
                    history.append({"role": "tool", "content": result})
                    continue  # Ask LLM again with updated history
            # Not a tool call: treat as final answer and break
            final_response = response
            break

        if final_response is not None:
            if stream:
                for c in final_response:
                    print(c, end="", flush=True)
                print()
                return ""
            return final_response
        return "⚠️ Max turns exceeded."

# --- Example Tools ---
def echo_tool(text: str) -> str:
    return f"ECHO: {text}"

def time_tool(_: str) -> str:
    now = datetime.now()
    return f"The current time is {now.strftime('%Y-%m-%d %H:%M:%S')}"

if __name__ == "__main__":
    # Define available tools
    tools = [
        Tool("Echo", echo_tool, "Returns the input text prefixed with ECHO. Usage: Echo(text)"),
        Tool("Time", time_tool, "Returns the current date and time. Usage: Time()"),
    ]
    # Build tool descriptions for the instructions
    tool_descriptions = "\n".join(
        f"- {tool.name}: {tool.description}" for tool in tools
    )
    # Instructions for the agent, including tool references
    instructions = (
        "You are an agent that may call tools by responding with TOOL_NAME(argument).\n"
        "Available tools:\n"
        f"{tool_descriptions}\n"
        "If no tool is needed, respond with the final answer."
    )
    # Create the agent
    agent = Agent(
        model="DeepSeek-R1-Distill-Llama-8B-GGUF/DeepSeek-R1-Distill-Llama-8B-Q8_0.gguf",
        tools=tools,
        instructions=instructions
    )

    # Run the agent with some user input (normal output)
    result = asyncio.run(agent.run("Please echo ‘hello world’."))
    print("Agent result:", result)

    # # Example: Run the agent with streaming output
    # asyncio.run(agent.run("What time is it?", stream=True))
