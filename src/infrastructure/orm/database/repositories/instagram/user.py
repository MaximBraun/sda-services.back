# coding utf-8

from ...models import InstagramUsers

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class InstagramUserRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            InstagramUsers,
        )

    async def fetch_all(
        self,
        related: list[str],
    ) -> list[InstagramUsers]:
        return await self.fetch_one_to_many(
            related=related,
        )
