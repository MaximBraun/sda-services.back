# coding utf-8

from ......interface.controllers.api.v1 import PixverseApplicationController

from ......interface.schemas.api import (
    Application,
    PixverseApplication,
    ChangeApplication,
)


class PixverseApplicationView:
    def __init__(
        self,
        controller: PixverseApplicationController,
    ) -> None:
        self._controller = controller

    async def fetch_applications(
        self,
        token_data: dict[str, int | str],
    ) -> list[Application]:
        return await self._controller.fetch_applications(
            token_data,
        )

    async def fetch_application_by_app_id(
        self,
        app_id: str,
    ) -> Application:
        return await self._controller.fetch_application_by_app_id(
            app_id,
        )

    async def add_application(
        self,
        data: PixverseApplication,
        token_data: dict[str, int | str],
    ) -> PixverseApplication:
        return await self._controller.add_application(
            data,
            token_data,
        )

    async def update_application(
        self,
        id: int,
        data: ChangeApplication,
        token_data: dict[str, int | str],
    ) -> PixverseApplication:
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
