# coding utf-8

from ......infrastructure.orm.database.repositories import PixverseTemplateRepository

from .....schemas.api import (
    Template,
    ITemplate,
    AddTemplate,
    ChangeTemplate,
)


class PixverseTemplateController:
    def __init__(
        self,
        repository: PixverseTemplateRepository,
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

    async def fetch_template_by_id(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> Template | None:
        return await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )

    async def add_template(
        self,
        data: ITemplate,
        preview_small: str,
        preview_large: str,
        token_data: dict[str, int | str],
    ) -> AddTemplate:
        return await self._repository.add_record(
            AddTemplate(
                **data.dict,
                preview_small=preview_small,
                preview_large=preview_large,
                auth_user_id=token_data.get("aid"),
            ),
        )

    async def update_template(
        self,
        id: int,
        data: ITemplate,
        preview_small: str,
        preview_large: str,
        token_data: dict[str, int | str],
    ) -> ChangeTemplate:
        template = await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )
        if template is not None:
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
        token_data: dict[str, int | str],
    ) -> bool:
        template = await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )
        if template is not None:
            return await self._repository.delete_record(
                id,
            )
        return False
