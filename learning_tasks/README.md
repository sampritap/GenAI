# Learning Tasks - Day 4 Async

6 practical tasks to understand async/await in Python and FastAPI.

## Pure Python Tasks

### Task 1: Async Basics
```bash
python learning_tasks/task_1_async_basics.py
```
**Learn:** `async def`, `await`, `asyncio.run()`

### Task 2: Sequential vs Concurrent
```bash
python learning_tasks/task_2_sequential_vs_concurrent.py
```
**Learn:** `asyncio.gather()` makes tasks run together (2s vs 3s)

### Task 3: I/O vs CPU Bound
```bash
python learning_tasks/task_3_io_vs_cpu.py
```
**Learn:** Async helps I/O (network), not CPU (calculation)

## FastAPI Tasks

### Task 4: Sync vs Async Endpoints
```bash
uvicorn learning_tasks.task_4_fastapi_sync_vs_async:app --reload
```
**In another terminal:**
```bash
curl http://localhost:8000/sync &
curl http://localhost:8000/async &
```
**Learn:** Async endpoints respond faster to concurrent requests

### Task 5: Async Dependencies
```bash
uvicorn learning_tasks.task_5_async_dependencies:app --reload
curl http://localhost:8000/users
```
**Learn:** Dependencies can be `async def` too

### Task 6: Concurrent Requests
```bash
uvicorn learning_tasks.task_6_concurrent_requests:app --reload
curl http://localhost:8000/profile/1
```
**Learn:** Use `asyncio.gather()` to run multiple API calls in parallel

## Key Concepts

| Concept | What | When |
|---------|------|------|
| `async def` | Declares coroutine | Always for I/O operations |
| `await` | Pauses execution | Inside `async def` functions |
| `asyncio.gather()` | Run tasks concurrently | Multiple I/O operations |
| `asyncio.sleep()` | Non-blocking pause | Simulates I/O (network, DB) |
| `time.sleep()` | Blocking pause | Don't use in async! |

## How to Practice

1. Run each task sequentially
2. Modify the code and observe changes
3. Add print statements to see execution order
4. Time the results to see concurrency benefits
5. Commit to GitHub when done

## Next Steps

After completing these tasks:
- Move to Day 5 (auth, rate limiting, real APIs)
- Fix your `backend/main.py` with `AsyncOpenAI`
- Add streaming responses
