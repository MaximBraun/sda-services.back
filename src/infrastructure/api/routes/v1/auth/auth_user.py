# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ......domain.entities.auth import (
    UserAuthToken,
)

from ....views.v1 import AuthUserView

from .....factroies.api.v1 import AuthUserViewFactory

from ......interface.schemas.api import (
    AuthUserCredentials,
    UserRefreshToken,
)

auth_user_router = APIRouter(tags=["Authorization"])


@auth_user_router.post(
    "/token",
    response_model=UserAuthToken,
)
async def create_user_tokens(
    credentials: AuthUserCredentials,
    view: AuthUserView = Depends(AuthUserViewFactory.create),
) -> UserAuthToken:
    return await view.create_user_tokens(
        credentials,
    )


@auth_user_router.post(
    "/refresh",
    response_model=UserAuthToken,
    response_model_exclude_none=True,
    response_model_exclude="token_type",
)
async def create_access_token(
    refresh_token: UserRefreshToken,
    view: AuthUserView = Depends(AuthUserViewFactory.create),
) -> UserAuthToken:
    return await view.create_access_token(
        refresh_token,
    )
