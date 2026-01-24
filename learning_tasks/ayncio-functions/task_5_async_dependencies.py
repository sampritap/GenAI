"""
DAY 4 - TASK 5: FastAPI Async Dependencies

Theory:
- Dependencies can be async (use async def)
- FastAPI awaits them automatically
- Great for database connections, API calls, etc.
"""

from fastapi import FastAPI, Depends
import asyncio

app = FastAPI()

async def get_database():
    """Simulate async database connection"""
    print("Connecting to DB...")
    await asyncio.sleep(0.5)
    return {"connection": "postgresql://localhost"}

async def get_current_user():
    """Simulate async auth check"""
    print("Checking auth...")
    await asyncio.sleep(0.3)
    return {"user": "john", "role": "admin"}

@app.get("/users")
async def get_users(
    db = Depends(get_database),
    user = Depends(get_current_user)
):
    """Both dependencies run concurrently"""
    return {
        "database": db,
        "current_user": user,
        "users": ["Alice", "Bob", "Charlie"]
    }

# Run: uvicorn learning_tasks.task_5_async_dependencies:app --reload
# Test: curl http://localhost:8000/users
