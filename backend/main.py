from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from backend.schemas import ChatRequest
import asyncio

from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# If using OpenAI SDK
from openai import OpenAI
print("OPENAI_API_KEY LOADED:", os.getenv("OPENAI_API_KEY") is not None)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

#prompt builder
def build_prompt(messages):
    """
    Converts structured messages into a single prompt string
    """
    prompt = ""
    for msg in messages:
        prompt += f"{msg.role.upper()}: {msg.content}\n"
    prompt += "ASSISTANT:"
    return prompt

#streaming LLM generator
async def stream_llm_response(prompt: str):
    """
    Async generator that streams LLM tokens
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
            await asyncio.sleep(0)  # allow event loop to breathe


#streaming endpoint
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    prompt = build_prompt(request.messages)
    return StreamingResponse(stream_llm_response(prompt), media_type="text/plain")