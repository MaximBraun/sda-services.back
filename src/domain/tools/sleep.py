# coding utf-8

from asyncio import sleep

from random import uniform

from functools import wraps

from typing import (
    Callable,
    Coroutine,
)


def waiter(
    min_sec: float = 1.0,
    max_sec: float = 2.0,
):
    def decorator(
        func: Callable[..., Coroutine],
    ):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            await sleep(uniform(min_sec, max_sec))

            result = await func(*args, **kwargs)

            await sleep(uniform(min_sec, max_sec))

            return result

        return wrapper

    return decorator
