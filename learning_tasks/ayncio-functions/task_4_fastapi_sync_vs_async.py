"""
DAY 4 - TASK 4: FastAPI Sync vs Async

Theory:
- def endpoint: runs in threadpool (blocking OK)
- async def endpoint: runs in event loop (must use await)
- Async endpoints handle concurrent requests faster
"""

from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/sync")
def sync_endpoint():
    """Takes 2 seconds, blocks other requests"""
    print(f"[SYNC] Start at {time.time():.1f}")
    time.sleep(2)
    print(f"[SYNC] End at {time.time():.1f}")
    return {"type": "sync"}

@app.get("/async")
async def async_endpoint():
    """Takes 2 seconds, doesn't block others"""
    print(f"[ASYNC] Start at {time.time():.1f}")
    await asyncio.sleep(2)
    print(f"[ASYNC] End at {time.time():.1f}")
    return {"type": "async"}

# Run: uvicorn learning_tasks.task_4_fastapi_sync_vs_async:app --reload
# Test in another terminal:
#   curl http://localhost:8000/sync &
#   curl http://localhost:8000/async &
# Async responds faster!
