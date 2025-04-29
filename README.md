# Local Agent

A simple Python agent framework that connects to a local LLM (via LM Studio/OpenAI API) and can call custom Python tools/functions based on LLM output. The agent interprets LLM responses, detects tool calls, executes them, and streams or returns the final answer.

⚠️ **NOTE: This project is in active development** ⚠️

Some or all of the features may be incomplete or not working. Feel free to submit PRs to help me build!

## Features

- Connects to a local LLM server (e.g., LM Studio)
- Supports multi-turn tool use and reasoning
- Easily extensible with custom tools
- Optionally streams the final response to the user

---

## Requirements

- Python 3.8+
- `openai` Python package
- A running LM Studio server (or compatible OpenAI API endpoint)

Install dependencies:
```sh
pip install openai
```

---

## Usage

1. **Start LM Studio** (or another OpenAI-compatible API server) on your machine.

2. **Edit the model path** in `main.py` if needed:
   ```python
   model="DeepSeek-R1-Distill-Llama-8B-GGUF/DeepSeek-R1-Distill-Llama-8B-Q8_0.gguf"
   ```

3. **Run the script:**
   ```sh
   python main.py
   ```

   Example output:
   ```
   Agent result: ECHO: ‘hello world’
   ```

4. **To stream the final response instead of printing it all at once:**
   Uncomment the streaming example at the bottom of `main.py`:
   ```python
   # asyncio.run(agent.run("What time is it?", stream=True))
   ```

---

## Adding More Tools

You can add new tools by defining a Python function and registering it with the agent.

### 1. Define your tool function

```python
def my_tool(arg: str) -> str:
    # Your logic here
    return f"Processed: {arg}"
```

### 2. Create a `Tool` object

```python
my_tool_obj = Tool(
    "MyTool",
    my_tool,
    "Describe what your tool does. Usage: MyTool(argument)"
)
```

### 3. Add it to the `tools` list

```python
tools = [
    Tool("Echo", echo_tool, "Returns the input text prefixed with ECHO. Usage: Echo(text)"),
    Tool("Time", time_tool, "Returns the current date and time. Usage: Time()"),
    my_tool_obj,  # Add your tool here
]
```

### 4. Update the instructions (handled automatically in the script)

The script will automatically include your tool in the agent's instructions.

---

## How Tool Calls Work

- The LLM is instructed to call tools by responding with `ToolName(argument)`.
- The agent detects this pattern, runs the corresponding Python function, and feeds the result back to the LLM.
- If the LLM responds with a normal answer (not a tool call), the agent returns or streams it to the user.

---

## Example Tool Call

If the user asks:  
```
What time is it?
```
The LLM may respond with:  
```
Time()
```
The agent runs the `time_tool` and returns the current time.

---