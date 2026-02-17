# coding utf-8

from asyncio import gather

from ...models import PhotoGeneratorTemplates

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)

from ......domain.constants import BODY_TOYBOX_NAME_PROMPT


class PhotoGeneratorTemplateRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PhotoGeneratorTemplates,
        )

    async def fetch_template(
        self,
        field_name: str,
        value: str | int,
        box_name: str | None = None,
    ) -> PhotoGeneratorTemplates | None:
        data: PhotoGeneratorTemplates | None = await self.fetch_field(
            field_name,
            value,
            many=False,
        )
        if box_name is not None:
            data.prompt += BODY_TOYBOX_NAME_PROMPT.format(box_name=box_name)
        return data

    async def fetch_templates_by_id(
        self,
        data: list[int],
    ) -> list[PhotoGeneratorTemplates]:
        return await gather(
            *[
                self.fetch_template(
                    "id",
                    id,
                )
                for id in data
            ]
        )
