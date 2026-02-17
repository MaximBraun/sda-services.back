# coding utf-8

from ......interface.controllers.api.v1 import PixverseStyleController

from ......interface.schemas.api import (
    IStyle,
    Style,
    ChangeStyle,
)


class PixverseStyleView:
    def __init__(
        self,
        controller: PixverseStyleController,
    ) -> None:
        self._controller = controller

    async def fetch_styles(
        self,
        token_data: dict[str, str | int],
    ) -> list[Style]:
        return await self._controller.fetch_styles(
            token_data,
        )

    async def fetch_style_by_id(
        self,
        id: int,
        token_data: dict[str, str | int],
    ) -> Style:
        return await self._controller.fetch_style_by_id(
            id,
            token_data,
        )

    async def add_style(
        self,
        data: IStyle,
        preview_small: str,
        preview_large: str,
        token_data: dict[str, str | int],
    ) -> ChangeStyle:
        return await self._controller.add_style(
            data,
            preview_small,
            preview_large,
            token_data,
        )

    async def update_style(
        self,
        id: int,
        data: Style,
        preview_small: str,
        preview_large: str,
        token_data: dict[str, str | int],
    ) -> ChangeStyle:
        return await self._controller.update_style(
            id,
            data,
            preview_small,
            preview_large,
            token_data,
        )

    async def delete_style(
        self,
        id: int,
        token_data: dict[str, str | int],
    ) -> bool:
        return await self._controller.delete_style(
            id,
            token_data,
        )
