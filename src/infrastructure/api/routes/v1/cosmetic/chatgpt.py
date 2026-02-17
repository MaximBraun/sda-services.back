# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    Query,
)

from ....views.v1 import CosmeticView

from ......interface.schemas.external import (
    ChatGPTCosmetic,
)

from .....factroies.api.v1 import CosmeticViewFactory


cosmetic_router = APIRouter(tags=["Cosmetic"])


@cosmetic_router.post(
    "/photo2cosmetic",
    response_model=list[ChatGPTCosmetic],
    response_model_exclude_none=True,
)
async def photo_to_cosmetic(
    image: UploadFile,
    app_id: str = Query(alias="appId"),
    user_id: str = Query(alias="userId"),
    view: CosmeticView = Depends(CosmeticViewFactory.create),
) -> list[ChatGPTCosmetic]:
    return await view.photo_to_cosmetic(
        image,
        app_id,
        user_id,
    )
