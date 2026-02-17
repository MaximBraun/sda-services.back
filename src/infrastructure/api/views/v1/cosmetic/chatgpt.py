# coding utf-8

from fastapi import UploadFile

from ......interface.controllers.api.v1 import CosmeticController

from ......interface.schemas.external import ChatGPTCosmetic


class CosmeticView:
    def __init__(
        self,
        controller: CosmeticController,
    ) -> None:
        self._controller = controller

    async def photo_to_cosmetic(
        self,
        image: UploadFile,
    ) -> list[ChatGPTCosmetic]:
        return await self._controller.photo_to_cosmetic(
            image,
        )
