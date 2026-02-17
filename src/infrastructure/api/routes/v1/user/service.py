# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_pagination import Page

from ......domain.tools import validate_token

from ....views.v1 import (
    UserServiceView,
    UserRouteView,
)

from .....factroies.api.v1 import (
    UserServiceViewFactory,
    UserRouteViewFactory,
)

from ......interface.schemas.api import (
    UserService,
    ServiceRoute,
)

user_service_router = APIRouter(tags=["User"])


@user_service_router.get(
    "/services",
    response_model=Page[UserService],
)
async def fetch_user_services(
    token_data: dict[str, str | int] = Depends(validate_token),
    view: UserServiceView = Depends(UserServiceViewFactory.create),
) -> Page[UserService]:
    return await view.fetch_services(
        token_data,
    )


@user_service_router.get(
    "/services/{title}/routes",
    response_model=Page[ServiceRoute],
)
async def fetch_user_services_routes(
    title: str,
    _: dict[str, str | int] = Depends(validate_token),
    view: UserRouteView = Depends(UserRouteViewFactory.create),
) -> Page[ServiceRoute]:
    return await view.fetch_routes(
        title,
    )
