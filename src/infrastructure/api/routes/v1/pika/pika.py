# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Request,
    Depends,
    Query,
)

from ....views.v1 import PikaView

from ......domain.tools import (
    auto_docs,
    check_user_tokens,
)

from ......interface.schemas.external import (
    PikaT2VBody,
    PikaV2VBody,
    IPikaResponse,
    PikaVideoResponse,
)

from .....factroies.api.v1 import PikaViewFactory


pika_router = APIRouter(tags=["Pika"])


@pika_router.post(
    "/text2video",
    response_model=IPikaResponse,
    response_model_exclude_none=True,
)
async def text_to_video(
    request: Request,
    body: PikaT2VBody,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: PikaView = Depends(PikaViewFactory.create),
) -> IPikaResponse:
    return await view.text_to_video(
        body,
        user_id,
        app_id,
    )


@pika_router.post(
    "/image2video",
    response_model=IPikaResponse,
    response_model_exclude_none=True,
)
async def image_to_video(
    request: Request,
    body: PikaT2VBody,
    image: UploadFile,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: PikaView = Depends(PikaViewFactory.create),
) -> IPikaResponse:
    return await view.image_to_video(
        body,
        image,
        user_id,
        app_id,
    )


@pika_router.post(
    "/template2video",
    response_model=IPikaResponse,
    response_model_exclude_none=True,
)
async def template_to_video(
    request: Request,
    body: PikaV2VBody,
    image: UploadFile,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: PikaView = Depends(PikaViewFactory.create),
) -> IPikaResponse:
    return await view.template_to_video(
        body,
        image,
        user_id,
        app_id,
    )


@pika_router.post(
    "/twist2video",
    response_model=IPikaResponse,
    response_model_exclude_none=True,
)
async def twist_to_video(
    request: Request,
    body: PikaT2VBody,
    video: UploadFile,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: PikaView = Depends(PikaViewFactory.create),
) -> IPikaResponse:
    return await view.twist_to_video(
        body,
        video,
        user_id,
        app_id,
    )


@pika_router.post(
    "/addition2video",
    response_model=IPikaResponse,
    response_model_exclude_none=True,
)
async def addition_to_video(
    request: Request,
    body: PikaT2VBody,
    files: list[UploadFile],
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: PikaView = Depends(PikaViewFactory.create),
) -> IPikaResponse:
    return await view.addition_to_video(
        body,
        files,
        user_id,
        app_id,
    )


@pika_router.post(
    "/face2swap",
    response_model=IPikaResponse,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=20)
async def swap_to_video(
    request: Request,
    files: list[UploadFile],
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: PikaView = Depends(PikaViewFactory.create),
) -> IPikaResponse:
    return await view.swap_to_video(
        files,
        user_id,
        app_id,
    )


@pika_router.get(
    "/status/{id}",
    response_model=PikaVideoResponse,
)
async def fetch_video_status(
    request: Request,
    id: str,
    view: PikaView = Depends(PikaViewFactory.create),
) -> PikaVideoResponse:
    return await view.fetch_video_status(
        id,
    )
