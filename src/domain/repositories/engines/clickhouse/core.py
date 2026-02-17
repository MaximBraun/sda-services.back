# coding utf-8

from functools import cached_property

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from ....entities.core import (
    IConfEnv,
    IEngine,
)


class IClickHouse(IEngine):
    def __init__(
        self,
        conf: IConfEnv,
    ) -> None:
        super().__init__(
            conf,
        )

    @cached_property
    def engine(
        self,
    ) -> AsyncEngine:
        return create_async_engine(
            self._conf.clickhouse_dsn_url,
            future=True,
        )

    @cached_property
    def session_factory(
        self,
    ) -> sessionmaker:
        return sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
