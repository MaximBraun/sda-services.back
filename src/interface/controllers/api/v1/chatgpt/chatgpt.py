# coding utf-8

from fastapi import UploadFile

from ......domain.entities.chatgpt import (
    IBody,
    T2PBody,
    TB2PBody,
    I2CBody,
    R2PBody,
)

from ......infrastructure.external.chatgpt import ChatGPTClient


class ChatGPTController:
    def __init__(
        self,
        client: ChatGPTClient,
    ) -> None:
        self._client = client

    async def text_to_photo(
        self,
        body: IBody,
        prompt: str,
    ):
        return await self._client.text_to_photo(
            body,
            prompt,
        )

    async def photo_to_photo(
        self,
        body: IBody,
        image: UploadFile,
        prompt: str,
    ):
        return await self._client.photo_to_photo(
            body,
            image,
            prompt,
        )

    async def template_to_photo(
        self,
        body: T2PBody,
        image: UploadFile,
    ):
        return await self._client.template_to_photo(
            body,
            image,
        )

    async def template_toybox_to_photo(
        self,
        body: TB2PBody,
        image: UploadFile,
    ):
        return await self._client.toybox_to_photo(
            body,
            image,
        )

    async def reshape_photo(
        self,
        body: R2PBody,
        image: UploadFile,
    ):
        return await self._client.reshape_photo(
            body,
            image,
        )

    async def face_to_swap(
        self,
        body: I2CBody,
        image: list[UploadFile],
    ):
        return await self._client.face_to_swap(
            body,
            image,
        )

    async def photo_to_antiques(
        self,
        image: UploadFile,
    ):
        return await self._client.photo_to_antiques(
            image,
        )
