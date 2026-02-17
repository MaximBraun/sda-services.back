# coding utf-8

from asyncio import gather

from ...models import WanTemplates

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class WanTemplateRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            WanTemplates,
        )

    async def fetch_template(
        self,
        field_name: str,
        value: str | int,
    ) -> WanTemplates | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_templates_by_id(
        self,
        data: list[int],
    ) -> list[WanTemplates]:
        return await gather(
            *[
                self.fetch_template(
                    "id",
                    id,
                )
                for id in data
            ]
        )
