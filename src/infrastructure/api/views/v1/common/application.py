# coding utf-8

from ......interface.controllers.api.v1 import ApplicationController

from ......interface.schemas.api import (
    StoreApplication,
    ChangeStoreApplication,
    AddStoreApplication,
)


class ApplicationView:
    def __init__(
        self,
        controller: ApplicationController,
    ) -> None:
        self._controller = controller

    async def fetch_applications(
        self,
        token_data: dict[str, int | str],
    ) -> list[StoreApplication]:
        return await self._controller.fetch_applications(
            token_data,
        )

    async def fetch_application(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> StoreApplication:
        return await self._controller.fetch_application(
            id,
            token_data,
        )

    async def add_application(
        self,
        data: AddStoreApplication,
        token_data: dict[str, int | str],
    ) -> AddStoreApplication:
        return await self._controller.add_application(
            data,
            token_data,
        )

    async def update_application(
        self,
        id: int,
        data: ChangeStoreApplication,
        token_data: dict[str, int | str],
    ) -> ChangeStoreApplication:
        return await self._controller.update_application(
            id,
            data,
            token_data,
        )

    async def delete_application(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> bool:
        return await self._controller.delete_application(
            id,
            token_data,
        )
