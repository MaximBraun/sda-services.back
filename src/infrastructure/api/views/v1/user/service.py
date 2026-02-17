# coding utf-8

from fastapi_pagination import Page

from ......interface.schemas.api import UserService

from ......interface.controllers.api.v1 import UserServiceController


class UserServiceView:
    def __init__(
        self,
        controller: UserServiceController,
    ) -> None:
        self._controller = controller

    async def fetch_services(
        self,
        token_data: dict[str, str | int],
    ) -> Page[UserService]:
        return await self._controller.fetch_services(
            token_data,
        )
