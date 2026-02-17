# coding utf-8

from ...models import UserGenerations

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class UserGenerationRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            UserGenerations,
        )

    async def fetch_generation(
        self,
        field_name: str,
        value: str | int,
    ) -> UserGenerations | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )
