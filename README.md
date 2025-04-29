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

---

## Setup Instructions

1. **Start LM Studio**

   - Download and install [LM Studio](https://lmstudio.ai/) if you haven't already.
   - Open LM Studio.

2. **Download and Run a Model in LM Studio**

   - In LM Studio, go to the "Models" tab and download a compatible model (e.g., DeepSeek-R1-Distill-Llama-8B).
   - Once downloaded, click "Run" to start the model server.
   - Make sure the "OpenAI Compatible API" is enabled (check the API tab in LM Studio for the server URL, usually `http://localhost:1234/v1`).

3. **Create and Activate a Virtual Environment**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows, activate with:
   ```sh
   venv\Scripts\activate
   ```

4. **Install Dependencies**

   ```sh
   pip install openai
   ```

---

## Usage

1. **Start LM Studio** (or another OpenAI-compatible API server) on your machine.

2. **Edit the model name** in `main.py` if needed:
   ```python
   MODEL = "hugging-quants/llama-3.2-3b-instruct"
   ```

3. **Run the script:**
   ```sh
   python main.py
   ```

   Example output:
   ```
   Agent result: The current time is 2024-06-01 12:34:56
   ```

4. **To run with different user input:**
   Edit the `asyncio.run(agent.run(...))` line in `main.py` with your prompt.

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
from src.tools import Tool

my_tool_obj = Tool(
    "MyTool",
    my_tool,
    "Describe what your tool does. Usage: MyTool(argument)"
)
```

### 3. Add it to the `tools` list

```python
tools = [
    Tool("Echo", echo_tool, "Prints the input text prefixed with ECHO. Usage: Echo(text)"),
    Tool("Time", time_tool, "Prints the current date and time. Usage: Time()"),
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
