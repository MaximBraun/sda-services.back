# coding utf-8

from fastapi import UploadFile

from .....schemas.external import (
    Resp,
    T2VBody,
    R2VBody,
    GenerationStatus,
    TE2VBody,
)

from ......infrastructure.external.pixverse import PixVerseClient


class PixVerseController:
    def __init__(
        self,
        client: PixVerseClient,
    ) -> None:
        self._client = client

    async def text_to_video(
        self,
        body: T2VBody,
    ) -> Resp:
        return await self._client.text_to_video(
            body,
        )

    async def image_to_video(
        self,
        body: T2VBody,
        image: UploadFile,
    ) -> Resp:
        return await self._client.image_to_video(
            body,
            image,
        )

    async def generation_status(
        self,
        id: int,
    ) -> GenerationStatus:
        return await self._client.generation_status(
            id,
        )

    async def restyle_video(
        self,
        body: T2VBody,
        video: UploadFile,
    ) -> Resp:
        return await self._client.restyle_video(
            body,
            video,
        )

    async def template_video(
        self,
        body: TE2VBody,
        image: UploadFile,
    ) -> Resp:
        return await self._client.template_video(
            body,
            image,
        )

    async def extend_to_video(
        self,
        body: TE2VBody,
        video: UploadFile,
    ) -> Resp:
        return await self._client.extend_to_video(
            body,
            video,
        )

    async def transition_to_video(
        self,
        body: T2VBody,
        images: list[UploadFile],
    ) -> Resp:
        return await self._client.transition_to_video(
            body,
            images,
        )
