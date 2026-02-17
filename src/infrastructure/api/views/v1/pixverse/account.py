# coding utf-8

from ......interface.controllers.api.v1 import PixverseAccountController

from ......interface.schemas.api import (
    Account,
    IAccount,
    ChangeAccount,
)


class PixverseAccountView:
    def __init__(
        self,
        controller: PixverseAccountController,
    ) -> None:
        self._controller = controller

    async def fetch_accounts(
        self,
        token_data: dict[str, str | int],
    ) -> list[Account]:
        return await self._controller.fetch_accounts(
            token_data,
        )

    async def fetch_account(
        self,
        id: int,
        token_data: dict[str, str | int],
    ) -> Account:
        return await self._controller.fetch_account(
            id,
            token_data,
        )

    async def add_account(
        self,
        data: IAccount,
        token_data: dict[str, str | int],
    ) -> ChangeAccount:
        return await self._controller.add_account(
            data,
            token_data,
        )

    async def update_account(
        self,
        id: int,
        data: ChangeAccount,
        token_data: dict[str, int | str],
    ) -> ChangeAccount:
        return await self._controller.update_account(
            id,
            data,
            token_data,
        )

    async def delete_account(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> bool:
        return await self._controller.delete_account(
            id,
            token_data,
        )
