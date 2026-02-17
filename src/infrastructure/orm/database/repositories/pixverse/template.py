# coding utf-8

from asyncio import gather

from ...models import PixverseTemplates

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class PixverseTemplateRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PixverseTemplates,
        )

    async def fetch_template(
        self,
        field_name: str,
        value: str | int,
    ) -> PixverseTemplates | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_templates_by_id(
        self,
        data: list[int],
    ) -> list[PixverseTemplates]:
        return await gather(
            *[
                self.fetch_template(
                    "id",
                    id,
                )
                for id in data
            ]
        )
