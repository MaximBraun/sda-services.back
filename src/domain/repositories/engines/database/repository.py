# coding utf-8

from .core import IDatabase

from ....entities.core import (
    ITable,
    IRepository,
)


class DatabaseRepository(IRepository):
    def __init__(
        self,
        engine: IDatabase,
        model: ITable,
    ) -> None:
        super().__init__(
            engine,
            model,
        )
