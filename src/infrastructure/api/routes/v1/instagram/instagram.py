# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
)

from typing import Literal

from fastapi_pagination import Page

from ....views.v1 import (
    InstagramView,
    QwenView,
)

from ......domain.tools import auto_docs

from ......domain.entities.instagram import ISession

from ......interface.schemas.external import (
    IInstagramUser,
    ITrackingUser,
    InstagramAuthResponse,
    InstagramUserResponse,
    InstagramUpdateUserResponse,
    InstagramTrackingUserResponse,
    InstagramFollower,
    IInstagramPost,
    T2PBody,
    ChatGPTInstagram,
    ChartData,
)

from ......interface.schemas.api import SearchUser

from .....factroies.api.v1 import (
    InstagramViewFactory,
    QwenViewFactory,
)


instagram_router = APIRouter(tags=["Instagram"])


@instagram_router.post(
    "/users/session",
)
async def auth_user_session(
    body: ISession,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramAuthResponse:
    return await view.auth_user_session(
        body,
    )


@instagram_router.post(
    "/users/{uuid}/search/{username}",
    response_model=SearchUser,
    response_model_exclude_none=True,
)
async def find_user(
    body: IInstagramUser,
    uuid: str,
    username: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> SearchUser:
    return await view.find_user(
        uuid,
        username,
    )


@instagram_router.post(
    "/users/{uuid}/tracking/{user_id}",
)
async def add_user_tracking(
    body: IInstagramUser,
    uuid: str,
    user_id: int,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramTrackingUserResponse:
    return await view.add_user_tracking(
        uuid,
        user_id,
    )


@instagram_router.post(
    "/users/{uuid}/tracking",
)
async def fetch_user_tracking(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[ITrackingUser]:
    return await view.fetch_user_tracking(
        uuid,
    )


@instagram_router.delete(
    "/users/{uuid}/tracking/{user_id}",
)
async def remove_user_tracking(
    body: IInstagramUser,
    uuid: str,
    user_id: int,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> bool:
    return await view.remove_user_tracking(
        uuid,
        user_id,
    )


@instagram_router.post(
    "/tracking/{username}/statistics",
    response_model=InstagramUserResponse,
)
async def fetch_public_statistics(
    username: str,
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramUserResponse:
    return await view.fetch_public_statistics(
        body,
        username,
    )


@instagram_router.post(
    "/tracking/{username}/chart",
    response_model=Page[ChartData],
)
async def tracking_user_subscribers_chart(
    username: str,
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[ChartData]:
    return await view.tracking_user_subscribers_chart(
        body,
        username,
    )


@instagram_router.post(
    "/users/{uuid}/update",
)
async def update_user_data(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramUpdateUserResponse:
    return await view.update_user_data(
        body,
        uuid,
    )


@instagram_router.post(
    "/users/{uuid}/statistics",
)
async def fetch_statistics(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> InstagramUserResponse:
    return await view.fetch_statistics(
        body,
        uuid,
    )


@instagram_router.post(
    "/users/{uuid}/publications/{id}",
)
async def fetch_publication(
    body: IInstagramUser,
    uuid: str,
    id: int,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> IInstagramPost:
    return await view.fetch_publication(
        body,
        uuid,
        id,
    )


@instagram_router.post(
    "/users/{username}/publications/{id}",
)
async def fetch_tracking_publication(
    body: IInstagramUser,
    username: str,
    id: int,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> IInstagramPost:
    return await view.fetch_tracking_publication(
        body,
        username,
        id,
    )


@instagram_router.post(
    "/users/{uuid}/subscribers",
)
async def fetch_subscribers(
    body: IInstagramUser,
    uuid: str,
    relation_type: Literal["new", "old", "unsub"] = "old",
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_subscribers(
        body,
        uuid,
        relation_type,
    )


@instagram_router.post(
    "/tracking/{username}/subscribers",
)
async def fetch_tracking_subscribers(
    username: str,
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
    relation_type: Literal["new", "old", "unsub"] = "old",
) -> Page[InstagramFollower]:
    return await view.fetch_tracking_subscribers(
        body,
        username,
        relation_type,
    )


@instagram_router.post(
    "/users/{uuid}/secret-fans",
)
async def fetch_secret_fans(
    body: IInstagramUser,
    uuid: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_secret_fans(
        body,
        uuid,
    )


@instagram_router.post(
    "/users/{username}/secret-fans",
)
async def fetch_tracking_secret_fans(
    body: IInstagramUser,
    username: str,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_tracking_secret_fans(
        body,
        username,
    )


@instagram_router.post(
    "/users/{uuid}/subscribers/chart",
)
async def user_subscribers_chart(
    uuid: str,
    body: IInstagramUser,
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[ChartData]:
    return await view.user_subscribers_chart(
        uuid,
        body,
    )


@instagram_router.post(
    "/users/{uuid}/subscribtions",
)
async def fetch_subscribtions(
    body: IInstagramUser,
    uuid: str,
    relation_type: Literal["mutual", "not_followed_by"] = "mutual",
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_subscribtions(
        body,
        uuid,
        relation_type,
    )


@instagram_router.post(
    "/users/{username}/subscribtions",
)
async def fetch_tracking_subscribtions(
    body: IInstagramUser,
    username: str,
    relation_type: Literal["mutual", "not_followed_by"] = "mutual",
    view: InstagramView = Depends(InstagramViewFactory.create),
) -> Page[InstagramFollower]:
    return await view.fetch_tracking_subscribtions(
        body,
        username,
        relation_type,
    )


@instagram_router.post(
    "/users/{uuid}/text2post",
)
async def text_to_post(
    uuid: str,
    body: T2PBody,
    view: QwenView = Depends(QwenViewFactory.create),
) -> ChatGPTInstagram:
    app_id = body.app_id
    user_id = body.user_id
    return await view.text_to_post(
        body,
        app_id,
        user_id,
    )
