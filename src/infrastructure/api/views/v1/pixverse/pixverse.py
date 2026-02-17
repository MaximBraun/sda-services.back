# coding utf-8

from fastapi import UploadFile

from ......domain.entities.pixverse import IBody

from ......interface.schemas.external import (
    T2VBody,
    Resp,
    R2VBody,
    GenerationStatus,
    TE2VBody,
)

from ......interface.controllers.api.v1 import PixVerseController


class PixVerseView:
    def __init__(
        self,
        controller: PixVerseController,
    ) -> None:
        self._controller = controller

    async def text_to_video(
        self,
        body: T2VBody,
    ) -> Resp:
        return await self._controller.text_to_video(
            body,
        )

    async def image_to_video(
        self,
        body: IBody,
        image: UploadFile,
    ) -> Resp:
        return await self._controller.image_to_video(
            body,
            image,
        )

    async def restyle_video(
        self,
        body: R2VBody,
        video: UploadFile,
    ) -> Resp:
        return await self._controller.restyle_video(
            body,
            video,
        )

    async def template_video(
        self,
        body: TE2VBody,
        image: UploadFile,
    ) -> Resp:
        return await self._controller.template_video(
            body,
            image,
        )

    async def extend_to_video(
        self,
        body: TE2VBody,
        video: UploadFile,
    ) -> Resp:
        return await self._controller.extend_to_video(
            body,
            video,
        )

    async def transition_to_video(
        self,
        body: T2VBody,
        images: list[UploadFile],
    ) -> Resp:
        return await self._controller.transition_to_video(
            body,
            images,
        )

    async def generation_status(
        self,
        id: int,
    ) -> GenerationStatus:
        return await self._controller.generation_status(
            id,
        )
