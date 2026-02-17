# coding utf-8

from fastapi import UploadFile

from ......interface.controllers.api.v1 import CaloriesController

from ......interface.schemas.external import ChatGPTCalories


class CaloriesView:
    def __init__(
        self,
        controller: CaloriesController,
    ) -> None:
        self._controller = controller

    async def text_to_calories(
        self,
        description: str,
    ) -> ChatGPTCalories:
        return await self._controller.text_to_calories(
            description,
        )

    async def text_to_weight_calories(
        self,
        description: str,
    ):
        return await self._controller.text_to_weight_calories(
            description,
        )

    async def photo_to_calories(
        self,
        image: UploadFile,
    ) -> ChatGPTCalories:
        return await self._controller.photo_to_calories(
            image,
        )

    async def photo_to_weight_calories(
        self,
        image: UploadFile,
    ):
        return await self._controller.photo_to_weight_calories(
            image,
        )
