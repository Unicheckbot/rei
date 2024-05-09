import asyncio
from typing import Callable, TypeVar

T = TypeVar("T")


async def run_in_eventloop(func: Callable[..., T], *args: object) -> T:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)
