import openai
import os
from app.config import SYSTEM_PROMPT
from orator import pipeline

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_stream(messages):
    complete_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    response = pipeline(
        messages=complete_messages,
        stream=True,
    )

    for chunk in response:
        if chunk.choices[0].delta.get("content"):
            yield chunk.choices[0].delta.content
