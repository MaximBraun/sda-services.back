# coding utf-8

from .core import IClickHouse

from ....entities.core import (
    ITable,
    IRepository,
)


class ClickHouseRepository(IRepository):
    def __init__(
        self,
        engine: IClickHouse,
        model: ITable,
    ) -> None:
        super().__init__(
            engine,
            model,
        )
