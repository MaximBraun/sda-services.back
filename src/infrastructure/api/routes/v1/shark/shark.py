# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
    Query,
)


from ....views.v1 import QwenView

from ......interface.schemas.external import (
    SharkDectorFactMessage,
)

from .....factroies.api.v1 import QwenViewFactory


shark_router = APIRouter(tags=["Shark"])


@shark_router.get(
    "/fact2day",
    response_model=SharkDectorFactMessage,
    response_model_exclude_none=True,
)
async def text_to_photo(
    app_id: str = Query(alias="appId"),
    user_id: str = Query(alias="userId"),
    view: QwenView = Depends(QwenViewFactory.create),
) -> SharkDectorFactMessage:
    # return await view.fetch_day_fact(
    #     app_id,
    #     user_id,
    # )
    return SharkDectorFactMessage(
        message="Octopuses: They have three hearts and blue blood, which helps them circulate oxygen efficiently in cold, low-oxygen ocean environments."
    )
