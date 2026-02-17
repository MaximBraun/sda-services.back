# coding utf-8

from ......interface.controllers.api.v1 import PikaApplicationController

from ......interface.schemas.api import (
    Application,
)


class PikaApplicationView:
    def __init__(
        self,
        controller: PikaApplicationController,
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
