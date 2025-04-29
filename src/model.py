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
        return client.chat.completions.acreate(
            model=model, messages=messages,
            temperature=temperature, stream=True
        )
    
    # Non-streaming response
    resp = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature
    )
    return resp.choices[0].message.content