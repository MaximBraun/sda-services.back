# coding utf-8

from ......interface.controllers.api.v1 import PikaAccountController

from ......interface.schemas.api import (
    Account,
)


class PikaAccountView:
    def __init__(
        self,
        controller: PikaAccountController,
    ) -> None:
        self._controller = controller

    async def fetch_accounts(
        self,
        token_data: dict[str, str | int],
    ) -> list[Account]:
        return await self._controller.fetch_accounts(
            token_data,
        )
