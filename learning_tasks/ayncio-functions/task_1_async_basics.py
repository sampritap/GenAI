"""
DAY 4 - TASK 1: First Async Function

Theory:
- async def creates a coroutine (pausable function)
- await pauses execution at I/O operations
- asyncio.run() executes the coroutine
"""

import asyncio

async def say_hello():
    print("Hello!")
    await asyncio.sleep(1)  # Pause for 1 second
    print("Done!")

# Run it
asyncio.run(say_hello())
