# coding utf-8

from ...models import InstagramUserRelations

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class InstagramUserRelationsRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            InstagramUserRelations,
        )
