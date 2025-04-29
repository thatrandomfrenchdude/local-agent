from datetime import datetime
from typing import Callable
import os
import requests

class Tool:
    def __init__(self, name: str, func: Callable[[str], str], description: str):
        self.name = name
        self.func = func
        self.description = description

    def run(self, arg: str) -> str:
        return self.func(arg) if arg != "" else self.func()

def echo_tool(text: str) -> str:
    return f"ECHO: {text}"

def time_tool() -> str:
    now = datetime.now()
    return f"The current time is {now.strftime('%Y-%m-%d %H:%M:%S')}"

# Define available tools
tools = [
    Tool(
        "Echo",
        echo_tool,
        "Prints the input text prefixed with ECHO. Usage: return the string 'Echo(<text>)' where <text> is the text to echo."
    ),
    Tool(
        "Time",
        time_tool,
        "Prints the current date and time. Usage: return the string 'Time()'"
    )
]
# Build tool descriptions for the instructions
tool_descriptions = "\n".join(
    f"- {tool.name}: {tool.description}" for tool in tools
)