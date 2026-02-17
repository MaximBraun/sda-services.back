# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Request,
    Depends,
    Query,
)

from asyncio import sleep

from ......domain.tools import (
    auto_docs,
    check_user_tokens,
)


from ......domain.entities.qwen import (
    IT2IBody,
)

from ......domain.entities.chatgpt import IQwenBody

from ....views.v1 import (
    QwenView,
    WanView,
    ChatGPTView,
)

from ......interface.schemas.external import (
    QwenPhotoAPIResponse,
    ChatGPTResp,
)

from .....factroies.api.v1 import (
    QwenViewFactory,
    WanViewFactory,
    ChatGPTViewFactory,
)


qwen_router = APIRouter(tags=["Qwen"])


# @qwen_router.post(
#     "/text2photo",
#     response_model=QwenPhotoAPIResponse,
#     response_model_exclude_none=True,
# )
# @check_user_tokens(method_cost=5)
# async def text_to_photo(
#     request: Request,
#     body: IT2IBody,
#     app_id: str = Query(alias="appId"),
#     user_id: str = Query(alias="userId"),
#     view: QwenView = Depends(QwenViewFactory.create),
# ) -> QwenPhotoAPIResponse:
#     return await view.text_to_photo(
#         body,
#         app_id,
#         user_id,
#     )


# @qwen_router.post(
#     "/photo2photo",
#     response_model=QwenPhotoAPIResponse,
#     response_model_exclude_none=True,
# )
# @check_user_tokens(method_cost=5)
# async def photo_to_photo(
#     request: Request,
#     body: IT2IBody,
#     image: UploadFile,
#     app_id: str = Query(alias="appId"),
#     user_id: str = Query(alias="userId"),
#     view: QwenView = Depends(QwenViewFactory.create),
# ) -> QwenPhotoAPIResponse:
#     return await view.photo_to_photo(
#         body,
#         image,
#         app_id,
#         user_id,
#     )


@qwen_router.post(
    "/text2photo",
    response_model=QwenPhotoAPIResponse,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=5)
async def text_to_photo(
    request: Request,
    body: IT2IBody,
    # data: IQwenBody = Depends(),
    app_id: str = Query(),
    user_id: str = Query(),
    view: WanView = Depends(WanViewFactory.create),
) -> QwenPhotoAPIResponse:
    data = await view.text_to_image(
        body,
        user_id,
        app_id,
    )

    while True:
        status = await view.fetch_media_status(
            data.media_id,
        )
        if status.media_urls == "generating":
            await sleep(2)

            continue

        return QwenPhotoAPIResponse(
            media_url=status.media_urls[0],
        )


@qwen_router.post(
    "/photo2photo",
    response_model=QwenPhotoAPIResponse,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=5)
async def photo_to_photo(
    request: Request,
    image: UploadFile,
    body: IT2IBody,
    app_id: str = Query(),
    user_id: str = Query(),
    view: WanView = Depends(WanViewFactory.create),
) -> ChatGPTResp:
    data = await view.photo_to_photo(
        body,
        image,
        user_id,
        app_id,
    )

    while True:
        status = await view.fetch_media_status(
            data.media_id,
        )
        if status.media_urls == "generating":
            await sleep(2)

            continue

        return QwenPhotoAPIResponse(
            media_url=status.media_urls[0],
        )
