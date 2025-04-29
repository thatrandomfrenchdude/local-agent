import re
from typing import List
from src.model import chat_completion, Message
from src.tools import Tool

class Agent:
    def __init__(
        self,
        model: str,
        tools: List[Tool],
        instructions: str,
        max_turns: int = 1
    ):
        self.model = model
        self.tools = {tool.name: tool for tool in tools}
        self.instructions = instructions
        self.max_turns = max_turns

    async def run(
        self,
        user_input: str,
    ) -> str:
        history: List[Message] = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": user_input}
        ]

        # final_response = None
        tool_call_pattern = re.compile(r"^(\w+)\((.*)\)$", re.DOTALL)

        # for _ in range(self.max_turns):
        # call the model with the initial request
        response = chat_completion(self.model, history)
        
        # check the output for a response
        match = tool_call_pattern.match(response.strip())
        print(match, response.strip())
        if match:
            name, arg = match.groups()
            tool = self.tools.get(name)
            if tool:
                # Handle tools with or without arguments
                result = tool.run(arg) if arg else tool.run("")
                history.append({"role": "assistant", "content": response})
                history.append({"role": "tool", "content": result})
                continue # Ask LLM again with updated history
            # Not a tool call: treat as final answer and break
            # final_response = response

        # if final_response is not None:
        #     return final_response
        return "⚠️ Max turns exceeded."