# coding utf-8

from ......interface.controllers.api.v1 import PixverseTemplateController

from ......interface.schemas.api import (
    Template,
    ITemplate,
    ChangeTemplate,
)


class PixverseTemplateView:
    def __init__(
        self,
        controller: PixverseTemplateController,
    ) -> None:
        self._controller = controller

    async def fetch_templates(
        self,
        token_data: dict[str, int | str],
    ) -> list[Template]:
        return await self._controller.fetch_templates(
            token_data,
        )

    async def fetch_template_by_id(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> Template:
        return await self._controller.fetch_template_by_id(
            id,
            token_data,
        )

    async def add_template(
        self,
        data: ITemplate,
        preview_small: str,
        preview_large: str,
        token_data: dict[str, int | str],
    ) -> ChangeTemplate:
        return await self._controller.add_template(
            data,
            preview_small,
            preview_large,
            token_data,
        )

    async def update_template(
        self,
        id: int,
        data: ITemplate,
        preview_small: str,
        preview_large: str,
        token_data: dict[str, int | str],
    ) -> ChangeTemplate:
        return await self._controller.update_template(
            id,
            data,
            preview_small,
            preview_large,
            token_data,
        )

    async def delete_template(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> bool:
        return await self._controller.delete_template(
            id,
            token_data,
        )
