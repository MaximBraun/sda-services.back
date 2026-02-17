# coding utf-8

from ......infrastructure.orm.database.repositories import PixverseStyleRepository

from .....schemas.api import (
    Style,
    ChangeStyle,
    AddStyle,
    IStyle,
)


class PixverseStyleController:
    def __init__(
        self,
        repository: PixverseStyleRepository,
    ) -> None:
        self._repository = repository

    async def fetch_styles(
        self,
        token_data: dict[str, str | int],
    ) -> list[Style]:
        return await self._repository.fetch_with_filters(
            many=True,
            auth_user_id=token_data.get("aid"),
        )

    async def fetch_style_by_id(
        self,
        id: int,
        token_data: dict[str, str | int],
    ) -> Style | None:
        return await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )

    async def add_style(
        self,
        data: IStyle,
        preview_small: str,
        preview_large: str,
        token_data: dict[str, str | int],
    ) -> AddStyle:
        return await self._repository.add_record(
            AddStyle(
                **data.dict,
                preview_small=preview_small,
                preview_large=preview_large,
                auth_user_id=token_data.get("aid"),
            ),
        )

    async def update_style(
        self,
        id: int,
        data: Style,
        preview_small: str,
        preview_large: str,
        token_data: dict[str, str | int],
    ) -> ChangeStyle:
        style = await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )
        if style is not None:
            return await self._repository.update_record(
                id,
                ChangeStyle(
                    **data.dict,
                    preview_small=preview_small,
                    preview_large=preview_large,
                ),
            )

    async def delete_style(
        self,
        id: int,
        token_data: dict[str, str | int],
    ) -> bool:
        style = await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )
        if style is not None:
            return await self._repository.delete_record(
                id,
            )
        return False
