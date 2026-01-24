"""
DAY 4 - TASK 2: Sequential vs Concurrent

Theory:
- Sequential: Task A → Task B (total time = A + B)
- Concurrent: Task A + Task B run "together" (total time = max(A, B))
- asyncio.gather() runs multiple coroutines concurrently
"""

import asyncio
import time

async def task_a():
    print("Task A start")
    await asyncio.sleep(2)
    print("Task A done")

async def task_b():
    print("Task B start")
    await asyncio.sleep(1)
    print("Task B done")

# Sequential (3 seconds total)
async def sequential():
    print("\n=== SEQUENTIAL (3 seconds) ===")
    start = time.time()
    await task_a()
    await task_b()
    print(f"Total: {time.time() - start:.1f}s\n")

# Concurrent (2 seconds total)
async def concurrent():
    print("=== CONCURRENT (2 seconds) ===")
    start = time.time()
    await asyncio.gather(task_a(), task_b())
    print(f"Total: {time.time() - start:.1f}s\n")

# Try both
asyncio.run(sequential())
asyncio.run(concurrent())
