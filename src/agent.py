from typing import List
from src.model import chat_completion, Message
from src.tools import Tool

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