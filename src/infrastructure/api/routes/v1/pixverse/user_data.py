# coding utf-8

from fastapi import (
    APIRouter,
    Path,
    Depends,
    Query,
)

from ....views.v1 import UserDataView

from ......domain.tools import auto_docs, validate_token

from .....factroies.api.v1 import UserDataViewFactory

from ......domain.entities.core import IUserData

from ......interface.schemas.external import (
    UserStatistics,
    UserFilters,
    IPixverseBody,
)


user_data_router = APIRouter(tags=["User Data"])


@user_data_router.get(
    "/statistics",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/statistics",
    "GET",
    description="Роутер для получения стастистики по пользователям.",
)
async def fetch_user_data(
    view: UserDataView = Depends(UserDataViewFactory.create),
    user_id: str | None = Query(None),
    app_id: str | None = Query(None),
    app_name: str | None = Query(None),
    token_data: dict[str, int | str] = Depends(validate_token),
) -> list[UserStatistics]:
    return await view.fetch_user_data(
        user_id,
        app_id,
        app_name,
        token_data,
    )


@user_data_router.get(
    "/statistics/filters",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/statistics/filters",
    "GET",
    description="Роутер для получения фильтров для стастистики по пользователям.",
)
async def fetch_user_filters(
    app_name: str | None = Query(None),
    view: UserDataView = Depends(UserDataViewFactory.create),
    token_data: dict[str, int | str] = Depends(validate_token),
) -> UserFilters:
    return await view.fetch_user_filters(
        app_name,
        token_data,
    )


@user_data_router.get(
    "/users/{user_id}/tokens",
)
@auto_docs(
    "api/v1/users/{user_id}/tokens",
    "GET",
    description="Роутер для получения токенов пользователя.",
)
async def fetch_user_tokens(
    user_id: str = Path(...),
    app_id: str = Query(..., alias="appId"),
    view: UserDataView = Depends(UserDataViewFactory.create),
) -> IUserData:
    return await view.fetch_user_tokens(
        user_id,
        app_id,
    )
