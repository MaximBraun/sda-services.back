# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    Query,
)


from ....views.v1 import QwenView

from ......interface.schemas.external import (
    ChatGPTGemstone,
)

from .....factroies.api.v1 import QwenViewFactory


gamestone_router = APIRouter(tags=["Gamestone"])


@gamestone_router.post(
    "/photo2gamestone",
    response_model=ChatGPTGemstone,
    response_model_exclude_none=True,
)
async def photo_to_gamestone(
    image: UploadFile,
    app_id: str = Query(alias="appId"),
    user_id: str = Query(alias="userId"),
    view: QwenView = Depends(QwenViewFactory.create),
) -> ChatGPTGemstone:
    return await view.photo_to_gamestone(
        image,
        app_id,
        user_id,
    )
