# coding utf-8

from ......interface.schemas.external import (
    IPikaResponse,
    PikaVideoResponse,
)

from ......infrastructure.external.pika import PikaClient


class PikaController:
    def __init__(
        self,
        client: PikaClient,
    ) -> None:
        self._client = client

    async def text_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._client.text_to_video(
            *args,
            **kwargs,
        )

    async def image_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._client.image_to_video(
            *args,
            **kwargs,
        )

    async def template_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._client.template_to_video(
            *args,
            **kwargs,
        )

    async def twist_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._client.twist_to_video(
            *args,
            **kwargs,
        )

    async def addition_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._client.addition_to_video(
            *args,
            **kwargs,
        )

    async def swap_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._client.swap_to_video(
            *args,
            **kwargs,
        )

    async def fetch_video_status(
        self,
        *args,
        **kwargs,
    ) -> PikaVideoResponse:
        return await self._client.fetch_video_status(
            *args,
            **kwargs,
        )
