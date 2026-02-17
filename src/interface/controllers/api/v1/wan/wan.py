# coding utf-8

from .....schemas.external import (
    IWanResponse,
    IWanMediaResponse,
)

from ......infrastructure.external.wan import WanClient


class WanController:
    def __init__(
        self,
        client: WanClient,
    ) -> None:
        self._client = client

    async def text_to_image(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._client.text_to_image(
            *args,
            **kwargs,
        )

    async def photo_to_photo(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._client.photo_to_photo(
            *args,
            **kwargs,
        )

    async def template_to_photo(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._client.template_to_photo(
            *args,
            **kwargs,
        )

    async def template_to_avatar(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._client.template_to_avatar(
            *args,
            **kwargs,
        )

    async def text_to_video(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._client.text_to_video(
            *args,
            **kwargs,
        )

    async def image_to_video(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._client.image_to_video(
            *args,
            **kwargs,
        )

    async def template_to_video(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._client.template_to_video(
            *args,
            **kwargs,
        )

    async def fetch_media_status(
        self,
        *args,
        **kwargs,
    ) -> IWanMediaResponse:
        return await self._client.fetch_media_status(
            *args,
            **kwargs,
        )
