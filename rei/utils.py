import asyncio
from typing import Callable


async def run_in_eventloop(func: Callable, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)
