"""
DAY 4 - TASK 6: Multiple Concurrent Requests

Theory:
- asyncio.gather() runs multiple coroutines concurrently
- Each await point allows other tasks to run
- Great for calling multiple APIs in parallel
"""

from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

async def fetch_user(user_id: int):
    """Simulate fetching user from API"""
    await asyncio.sleep(1)
    return {"id": user_id, "name": f"User{user_id}"}

async def fetch_posts(user_id: int):
    """Simulate fetching posts from API"""
    await asyncio.sleep(1)
    return {"user_id": user_id, "posts": 5}

async def fetch_comments(user_id: int):
    """Simulate fetching comments from API"""
    await asyncio.sleep(1)
    return {"user_id": user_id, "comments": 12}

@app.get("/profile/{user_id}")
async def get_profile(user_id: int):
    """Fetch user, posts, comments in parallel"""
    start = time.time()
    
    # Sequential: 3 seconds (1+1+1)
    # Concurrent: 1 second (max of 1,1,1)
    user, posts, comments = await asyncio.gather(
        fetch_user(user_id),
        fetch_posts(user_id),
        fetch_comments(user_id)
    )
    
    elapsed = time.time() - start
    return {
        "user": user,
        "posts": posts,
        "comments": comments,
        "fetch_time": f"{elapsed:.1f}s"
    }

# Run: uvicorn learning_tasks.task_6_concurrent_requests:app --reload
# Test: curl http://localhost:8000/profile/1
# Should take ~1 second, not 3!
