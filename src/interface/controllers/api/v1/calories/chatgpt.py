# coding utf-8

from fastapi import UploadFile

from ......infrastructure.external.calories import CaloriesClient

from ......interface.schemas.external import ChatGPTCalories


class CaloriesController:
    def __init__(
        self,
        client: CaloriesClient,
    ) -> None:
        self._client = client

    async def text_to_calories(
        self,
        description: str,
    ) -> ChatGPTCalories:
        return await self._client.text_to_calories(
            description,
        )

    async def text_to_weight_calories(
        self,
        description: str,
    ):
        return await self._client.text_to_weight_calories(
            description,
        )

    async def photo_to_calories(
        self,
        image: UploadFile,
    ) -> ChatGPTCalories:
        return await self._client.photo_to_calories(
            image,
        )

    async def photo_to_weight_calories(
        self,
        image: UploadFile,
    ):
        return await self._client.photo_to_weight_calories(
            image,
        )
