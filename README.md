# Local Agent

A simple Python agent framework that connects to a local LLM (via LM Studio/OpenAI API) and can call custom Python tools/functions based on LLM output. The agent interprets LLM responses, detects tool calls, executes them, and streams or returns the final answer.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Adding More Tools](#adding-more-tools)
- [Contributing](#contributing)
- [License](#license)

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

   - In LM Studio, go to the "Models" tab and download a compatible model (e.g., llama-3.2-3b-instruct).
   - Once downloaded, click "Run" to start the model server.
   - Make sure the "OpenAI Compatible API" is enabled (check the API tab in LM Studio for the server URL, usually `http://localhost:1234/v1`).

3. **Create and Edit the Configuration File**

   Create a file named `config.yaml` in the project root with the following contents (edit values as needed):

   ```yaml
   MODEL: "hugging-quants/llama-3.2-3b-instruct"
   LM_STUDIO_URL: "http://localhost:1234/v1"
   LM_STUDIO_API_KEY: "lm-studio"
   ```

   - `MODEL`: The model name as shown in LM Studio.
   - `LM_STUDIO_URL`: The API URL for your LM Studio server.
   - `LM_STUDIO_API_KEY`: The API key (default for LM Studio is `"lm-studio"`).

4. **Create and Activate a Virtual Environment**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows, activate with:
   ```sh
   venv\Scripts\activate
   ```

5. **Install Dependencies**

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
    Tool(
        "Echo",
        echo_tool,
        "Prints the input text prefixed with ECHO. Usage: return the string 'Echo(<text>)' where <text> is the text to echo."
    ),
    Tool(
        "Time",
        time_tool,
        "Prints the current date and time. Usage: return the string 'Time()'"
    ),
    my_tool_obj,  # Add your tool here
]
```

### 4. Update the instructions (handled automatically in the script)

The script will automatically include your tool in the agent's instructions.

---

## Contributing
I welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes, commit them, and push to your branch.
4. Create a pull request explaining your changes.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---