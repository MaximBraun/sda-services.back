# coding utf-8

from ...models import Products

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class ProductRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            Products,
        )

    async def fetch_application(
        self,
        field_name: str,
        value: str | int,
    ) -> Products | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )
