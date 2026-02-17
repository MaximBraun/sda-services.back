# coding utf-8

from asyncio import Lock

from typing import Any

from collections import defaultdict


account_locks: dict[int, Lock] = defaultdict(Lock)


async def account_lock(
    account_id: int,
    coro,
) -> Any:
    async with account_locks[account_id]:
        return await coro()
