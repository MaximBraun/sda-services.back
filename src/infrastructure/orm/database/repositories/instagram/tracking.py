# coding utf-8

from ...models import InstagramTracking

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class InstagramTrackingRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            InstagramTracking,
        )
