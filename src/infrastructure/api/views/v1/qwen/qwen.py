# coding utf-8

from fastapi import UploadFile

from ......domain.entities.qwen import (
    IT2IBody,
    IT2TBody,
    II2RBody,
    IP2BBody,
    IT2CBody,
    IT2PBody,
)

from ......interface.schemas.external import (
    QwenPhotoAPIResponse,
    ChatGPTCalories,
    ChatGPTCosmetic,
    ChatGPTInstagram,
    ChatGPTGemstone,
    SharkDectorFactMessage,
    DialogImageAnalysisMessage,
)

from ......interface.controllers.api.v1 import QwenController


class QwenView:
    def __init__(
        self,
        controller: QwenController,
    ) -> None:
        self._controller = controller

    async def text_to_photo(
        self,
        body: IT2IBody,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        return await self._controller.text_to_photo(
            body,
            app_id,
            user_id,
        )

    async def photo_to_photo(
        self,
        body: IT2IBody,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        return await self._controller.photo_to_photo(
            body,
            image,
            app_id,
            user_id,
        )

    async def template_to_photo(
        self,
        body: IT2TBody,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        return await self._controller.template_to_photo(
            body,
            image,
            app_id,
            user_id,
        )

    async def photo_to_toybox(
        self,
        body: IP2BBody,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        return await self._controller.photo_to_toybox(
            body,
            image,
            app_id,
            user_id,
        )

    async def reshape_to_photo(
        self,
        body: II2RBody,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        return await self._controller.reshape_to_photo(
            body,
            image,
            app_id,
            user_id,
        )

    async def photo_to_cosmetic(
        self,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> list[ChatGPTCosmetic]:
        return await self._controller.photo_to_cosmetic(
            image,
            app_id,
            user_id,
        )

    async def text_to_calories(
        self,
        body: IT2CBody,
        app_id: str,
        user_id: str,
    ) -> ChatGPTCalories:
        return await self._controller.text_to_calories(
            body,
            app_id,
            user_id,
        )

    async def photo_to_calories(
        self,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> ChatGPTCalories:
        return await self._controller.photo_to_calories(
            image,
            app_id,
            user_id,
        )

    async def text_to_post(
        self,
        body: IT2PBody,
        app_id: str,
        user_id: str,
    ) -> ChatGPTInstagram:
        return await self._controller.text_to_post(
            body,
            app_id,
            user_id,
        )

    async def photo_to_gamestone(
        self,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> ChatGPTGemstone:
        return await self._controller.photo_to_gamestone(
            image,
            app_id,
            user_id,
        )

    async def fetch_day_fact(
        self,
        app_id: str,
        user_id: str,
    ) -> SharkDectorFactMessage:
        return await self._controller.fetch_day_fact(
            app_id,
            user_id,
        )

    async def photo_to_honesty(
        self,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> DialogImageAnalysisMessage:
        return await self._controller.photo_to_honesty(
            image,
            app_id,
            user_id,
        )
