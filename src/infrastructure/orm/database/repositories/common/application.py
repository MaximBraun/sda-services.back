# coding utf-8

from ...models import Applications, Products

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class ApplicationRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            Applications,
        )

    async def fetch_all(
        self,
        related: list[str],
    ) -> Applications:
        return await self.fetch_one_to_many(
            related=related,
        )

    async def fetch_application(
        self,
        field_name: str,
        value: str | int,
    ) -> Applications | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_application_by_bundle_id(
        self,
        field_name: str,
        value: str,
        related: list[str],
    ) -> Applications | None:
        return await self.fetch_one_to_many(
            field_name,
            value,
            many=False,
            related=related,
            models=(Applications, Products),
        )
