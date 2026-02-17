# coding utf-8

from ......domain.entities.auth import (
    UserAuthToken,
)

from ......interface.controllers.api.v1 import AuthUserController

from ......interface.schemas.api import (
    AuthUserCredentials,
    UserRefreshToken,
)


class AuthUserView:
    def __init__(
        self,
        controller: AuthUserController,
    ) -> None:
        self._controller = controller

    async def create_user_tokens(
        self,
        credentials: AuthUserCredentials,
    ) -> UserAuthToken:
        return await self._controller.create_user_tokens(
            credentials,
        )

    async def create_access_token(
        self,
        refresh_token: UserRefreshToken,
    ) -> UserAuthToken:
        return await self._controller.create_access_token(
            refresh_token,
        )
