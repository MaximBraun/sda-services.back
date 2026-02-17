# coding utf-8

from fastapi_pagination import Page

from ......interface.schemas.api import ServiceRoute

from ......interface.controllers.api.v1 import UserRouteController


class UserRouteView:
    def __init__(
        self,
        controller: UserRouteController,
    ) -> None:
        self._controller = controller

    async def fetch_routes(
        self,
        title: str,
    ) -> Page[ServiceRoute]:
        return await self._controller.fetch_routes(
            title,
        )
