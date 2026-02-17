# coding utf-8

from ...models import PixverseCategories

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class PixverseCategoriesRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PixverseCategories,
        )

    async def fetch_category(
        self,
        field_name: str,
        value: str | int,
    ) -> PixverseCategories | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )
