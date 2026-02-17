# coding utf-8

from ...models import UserEvents

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class UserEventRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            UserEvents,
        )
