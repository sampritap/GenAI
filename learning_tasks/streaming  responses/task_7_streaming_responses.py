"""
DAY 4 - TASK 7: Streaming vs Non-Streaming Responses

Theory:
- Non-Streaming: Entire response sent at once (client waits)
- Streaming: Data sent in chunks progressively (real-time)
- Great for AI responses, file downloads, real-time data
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import time

app = FastAPI()

# ============================================
# NON-STREAMING RESPONSE
# ============================================

@app.get("/non-stream/data")
async def non_streaming_data():
    """
    Regular endpoint - sends entire response at once
    Client waits until ALL data is ready
    """
    # Simulate generating data (takes 3 seconds)
    await asyncio.sleep(1)
    data_1 = {"id": 1, "name": "Alice"}
    
    await asyncio.sleep(1)
    data_2 = {"id": 2, "name": "Bob"}
    
    await asyncio.sleep(1)
    data_3 = {"id": 3, "name": "Charlie"}
    
    # Send all at once (client waited 3 seconds)
    return {
        "users": [data_1, data_2, data_3],
        "total_wait_time": "3 seconds"
    }


# ============================================
# STREAMING RESPONSE
# ============================================

@app.get("/stream/data")
async def streaming_data():
    """
    Streaming endpoint - sends data in chunks
    Client receives data progressively (real-time)
    """
    async def generate():
        # Chunk 1
        await asyncio.sleep(1)
        yield "data: User 1: Alice\n\n"
        
        # Chunk 2
        await asyncio.sleep(1)
        yield "data: User 2: Bob\n\n"
        
        # Chunk 3
        await asyncio.sleep(1)
        yield "data: User 3: Charlie\n\n"
        
        yield "data: [DONE]\n\n"
    
    # Client sees: Chunk 1 after 1s, Chunk 2 after 2s, Chunk 3 after 3s
    return StreamingResponse(generate(), media_type="text/event-stream")


# ============================================
# STREAMING WITH SIMULATED AI RESPONSE
# ============================================

@app.get("/stream/ai-response")
async def stream_ai_response(prompt: str = "Tell me about async programming"):
    """
    Simulates OpenAI streaming response
    Each token arrives progressively
    """
    async def generate():
        # Simulate AI response tokens arriving one by one
        response_text = "Async programming allows you to run multiple tasks concurrently without blocking. It uses await and async/await syntax to pause execution at I/O points. This is perfect for handling multiple requests in FastAPI servers efficiently."
        
        words = response_text.split()
        for word in words:
            await asyncio.sleep(0.1)  # Simulate token arrival delay
            yield f"{word} "
    
    return StreamingResponse(generate(), media_type="text/plain")


# ============================================
# STREAMING WITH JSON CHUNKS
# ============================================

@app.get("/stream/json")
async def streaming_json():
    """
    Stream JSON objects line by line
    Useful for processing large datasets
    """
    async def generate():
        import json
        
        for i in range(5):
            await asyncio.sleep(0.5)
            user = {"id": i+1, "name": f"User{i+1}", "timestamp": time.time()}
            yield json.dumps(user) + "\n"
    
    return StreamingResponse(generate(), media_type="application/x-ndjson")


# ============================================
# COMPARISON TEST ENDPOINT
# ============================================

@app.get("/compare")
async def compare_responses():
    """
    Returns timing comparison info
    """
    return {
        "non_streaming": {
            "description": "Entire response sent at once",
            "client_wait_time": "3 seconds",
            "use_case": "Small data, simple APIs",
            "endpoint": "/non-stream/data"
        },
        "streaming": {
            "description": "Data sent in chunks progressively",
            "client_wait_time": "First chunk: 1s, Last chunk: 3s",
            "use_case": "Large data, AI responses, real-time updates",
            "endpoints": [
                "/stream/data",
                "/stream/ai-response",
                "/stream/json"
            ]
        }
    }


# ============================================
# HOW TO RUN AND TEST
# ============================================

"""
Run the server:
    uvicorn learning_tasks.ayncio-functions.task_7_streaming_responses:app --reload

Test endpoints:

1. Non-Streaming (waits 3 seconds):
    curl http://localhost:8000/non-stream/data

2. Streaming (progressive chunks):
    curl http://localhost:8000/stream/data

3. Streaming AI Response:
    curl http://localhost:8000/stream/ai-response?prompt="Hello"

4. Streaming JSON:
    curl http://localhost:8000/stream/json

5. Compare Info:
    curl http://localhost:8000/compare

Observation:
- Non-streaming: Get ALL data after waiting 3 seconds
- Streaming: Get data progressively (chunk after chunk)
"""
