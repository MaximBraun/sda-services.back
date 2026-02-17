# coding utf-8

from fastapi import (
    APIRouter,
    Request,
    UploadFile,
    Depends,
    Query,
)

from ....views.v1 import WanView

from ......domain.tools import (
    auto_docs,
    check_user_tokens,
)

from ......interface.schemas.external import (
    IWanResponse,
    IWanMediaResponse,
)

from ......domain.entities.wan import (
    IT2IBody,
    IT2VBody,
    IE2VBody,
)

from .....factroies.api.v1 import WanViewFactory


wan_router = APIRouter(tags=["Wan"])


@wan_router.post(
    "/text2image",
    response_model=IWanResponse,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=20)
async def text_to_image(
    request: Request,
    body: IT2IBody,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: WanView = Depends(WanViewFactory.create),
) -> IWanResponse:
    return await view.text_to_image(
        body,
        user_id,
        app_id,
    )


@wan_router.post(
    "/text2video",
    response_model=IWanResponse,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=20)
async def text_to_video(
    request: Request,
    body: IT2VBody,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: WanView = Depends(WanViewFactory.create),
) -> IWanResponse:
    return await view.text_to_video(
        body,
        user_id,
        app_id,
    )


@wan_router.post(
    "/image2video",
    response_model=IWanResponse,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=20)
async def image_to_video(
    request: Request,
    image: UploadFile,
    body: IT2VBody,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: WanView = Depends(WanViewFactory.create),
) -> IWanResponse:
    return await view.image_to_video(
        image,
        body,
        user_id,
        app_id,
    )


@wan_router.post(
    "/template2video",
    response_model=IWanResponse,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=20)
async def template_to_video(
    request: Request,
    image: UploadFile,
    body: IE2VBody,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: WanView = Depends(WanViewFactory.create),
) -> IWanResponse:
    return await view.template_to_video(
        image,
        body,
        user_id,
        app_id,
    )


@wan_router.get(
    "/status/{id}",
    response_model=IWanMediaResponse,
    response_model_exclude_none=True,
)
async def fetch_media_status(
    request: Request,
    id: str,
    view: WanView = Depends(WanViewFactory.create),
) -> IWanMediaResponse:
    return await view.fetch_media_status(
        id,
    )
