# coding utf-8

from typing import (
    Any,
    AsyncGenerator,
)

from functools import cached_property

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
)

from contextlib import asynccontextmanager

from .conf import IConfEnv

from ...errors import EngineError


class IEngine:
    def __init__(
        self,
        conf: IConfEnv,
    ) -> None:
        self._conf = conf

    @cached_property
    def engine(
        self,
    ) -> AsyncEngine:
        raise EngineError(
            self.__class__.__name__,
            "Engine",
        )

    @cached_property
    def session_factory(
        self,
    ) -> sessionmaker:
        raise EngineError(
            self.__class__.__name__,
            "SessionFactory",
        )

    @asynccontextmanager
    async def get_session(
        self,
    ) -> AsyncGenerator[AsyncSession, Any]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as err:
                await session.rollback()

                raise err
