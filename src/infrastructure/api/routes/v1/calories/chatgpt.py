# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    Query,
)

from ......domain.entities.qwen import (
    IT2CBody,
)

from ....views.v1 import CaloriesView

from ......interface.schemas.external import (
    ChatGPTCalories,
    ChatGPTWeightCalories,
)

from .....factroies.api.v1 import CaloriesViewFactory


calories_router = APIRouter(tags=["Calories"])


@calories_router.post(
    "/text2calories",
    response_model=ChatGPTCalories,
    response_model_exclude_none=True,
)
async def text_to_calories(
    body: IT2CBody = Depends(),
    app_id: str = Query(alias="appId"),
    user_id: str = Query(alias="userId"),
    view: CaloriesView = Depends(CaloriesViewFactory.create),
) -> ChatGPTCalories:
    return await view.text_to_calories(
        body.description,
        # app_id,
        # user_id,
    )


@calories_router.post(
    "/photo2calories",
    response_model=ChatGPTCalories,
    response_model_exclude_none=True,
)
async def photo_to_calories(
    image: UploadFile,
    app_id: str = Query(alias="appId"),
    user_id: str = Query(alias="userId"),
    view: CaloriesView = Depends(CaloriesViewFactory.create),
) -> ChatGPTCalories | str:
    return await view.photo_to_calories(
        image,
        # app_id,
        # user_id,
    )


@calories_router.post(
    "/text2weight",
    response_model=ChatGPTWeightCalories,
    response_model_exclude_none=True,
)
async def text_to_weight_calories(
    body: IT2CBody = Depends(),
    app_id: str = Query(alias="appId"),
    user_id: str = Query(alias="userId"),
    view: CaloriesView = Depends(CaloriesViewFactory.create),
) -> ChatGPTWeightCalories:
    return await view.text_to_weight_calories(
        body.description,
        # app_id,
        # user_id,
    )


@calories_router.post(
    "/photo2weight",
    response_model=ChatGPTWeightCalories,
    response_model_exclude_none=True,
)
async def photo_to_weight_calories(
    image: UploadFile,
    app_id: str = Query(alias="appId"),
    user_id: str = Query(alias="userId"),
    view: CaloriesView = Depends(CaloriesViewFactory.create),
) -> ChatGPTWeightCalories:
    return await view.photo_to_weight_calories(
        image,
        # app_id,
        # user_id,
    )
