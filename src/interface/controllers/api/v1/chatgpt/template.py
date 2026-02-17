# coding utf-8

from ......infrastructure.orm.database.repositories import (
    PhotoGeneratorTemplateRepository,
)

from .....schemas.api import (
    Template,
    ITemplate,
    ChangeTemplate,
)


class PhotoGeneratorTemplateController:
    def __init__(
        self,
        repository: PhotoGeneratorTemplateRepository,
    ) -> None:
        self._repository = repository

    async def fetch_templates(
        self,
        token_data: dict[str, int | str],
    ) -> list[Template]:
        return await self._repository.fetch_with_filters(
            many=True,
            auth_user_id=token_data.get("aid"),
        )

    async def fetch_template_by_template_id(
        self,
        template_id: int,
    ) -> Template | None:
        return await self._repository.fetch_template(
            "template_id",
            template_id,
        )

    async def fetch_template_by_id(
        self,
        id: int,
    ) -> Template | None:
        return await self._repository.fetch_template(
            "id",
            id,
        )

    async def add_template(
        self,
        data: ITemplate,
        preview_small: str,
        preview_large: str,
    ) -> ChangeTemplate:
        return await self._repository.add_record(
            ChangeTemplate(
                **data.dict,
                preview_small=preview_small,
                preview_large=preview_large,
            ),
        )

    async def update_template(
        self,
        id: int,
        data: Template,
        preview_small: str,
        preview_large: str,
    ) -> Template:
        return await self._repository.update_record(
            id,
            ChangeTemplate(
                **data.dict,
                preview_small=preview_small,
                preview_large=preview_large,
            ),
        )

    async def delete_template(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )
