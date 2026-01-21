from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"

@app.get("/")
def root():
    return {"message": "GenAI backend running"}

@app.post("/generate")
async def generate_tex(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=500
        )
        return {
            "prompt": request.prompt,
            "response": response.choices[0].message.content
        }
    except Exception as e:
        return {"error": str(e)}
