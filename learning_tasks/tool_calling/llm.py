import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # For OpenAI
    # base_url="http://localhost:11434/v1",  # Uncomment for Ollama
)

def call_llm(messages, tools):
    print("Calling OpenAI...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # change to "phi3" if using Ollama
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    print("openAi responded")

    return response.choices[0].message
