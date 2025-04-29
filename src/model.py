from typing import List, Dict, Any
from openai import OpenAI

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