from datetime import datetime
from typing import Callable

class Tool:
    def __init__(self, name: str, func: Callable[[str], str], description: str):
        self.name = name
        self.func = func
        self.description = description

    def run(self, arg: str) -> str:
        return self.func(arg)

def echo_tool(text: str) -> str:
    return f"ECHO: {text}"

def time_tool(_: str) -> str:
    now = datetime.now()
    return f"The current time is {now.strftime('%Y-%m-%d %H:%M:%S')}"

# Define available tools
tools = [
    Tool("Echo", echo_tool, "Returns the input text prefixed with ECHO. Usage: Echo(text)"),
    Tool("Time", time_tool, "Returns the current date and time. Usage: Time()"),
]
# Build tool descriptions for the instructions
tool_descriptions = "\n".join(
    f"- {tool.name}: {tool.description}" for tool in tools
)