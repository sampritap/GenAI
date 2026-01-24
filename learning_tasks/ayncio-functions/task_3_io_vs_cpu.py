"""
DAY 4 - TASK 3: I/O vs CPU Bound

Theory:
- I/O-bound (network, file): async helps (non-blocking)
- CPU-bound (calculation): async doesn't help (always busy)
- asyncio.to_thread() runs blocking code in separate thread
"""

import asyncio
import time

# I/O-bound (async is GOOD)
async def io_task():
    print("I/O: Starting network request...")
    await asyncio.sleep(2)
    print("I/O: Response received!")
    return "data"

# CPU-bound (async doesn't help)
def cpu_task():
    print("CPU: Starting computation...")
    result = sum(range(100_000_000))
    print("CPU: Done!")
    return result

async def main():
    start = time.time()
    
    # Run both concurrently
    results = await asyncio.gather(
        io_task(),
        asyncio.to_thread(cpu_task)
    )
    
    elapsed = time.time() - start
    print(f"\nBoth completed in {elapsed:.1f}s")
    print(f"Results: {results}")

asyncio.run(main())
