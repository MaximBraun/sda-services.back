# coding utf-8

from fastapi import (
    APIRouter,
    Request,
    UploadFile,
    Depends,
    Query,
)

from ....views.v1 import XimilarView

from ......domain.tools import (
    auto_docs,
    check_user_tokens,
)

from ......domain.entities.ximilar import CardResponse


from .....factroies.api.v1 import XimilarViewFactory


ximilar_router = APIRouter(tags=["Ximilar"])


@ximilar_router.post(
    "/card2info",
    response_model=CardResponse,
    # response_model_exclude_none=True,
)
@check_user_tokens(method_cost=10)
async def text_to_image(
    request: Request,
    image: UploadFile,
    user_id: str = Query(..., alias="userId"),
    app_id: str = Query(..., alias="appId"),
    view: XimilarView = Depends(XimilarViewFactory.create),
) -> CardResponse:
    return await view.image_to_card(
        image,
        user_id,
        app_id,
    )
