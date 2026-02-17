# # coding utf-8

from ......interface.controllers.api.v1 import PikaController

from ......interface.schemas.external import (
    IPikaResponse,
    PikaVideoResponse,
)


class PikaView:
    def __init__(
        self,
        controller: PikaController,
    ) -> None:
        self._controller = controller

    async def text_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._controller.text_to_video(
            *args,
            **kwargs,
        )

    async def image_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._controller.image_to_video(
            *args,
            **kwargs,
        )

    async def template_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._controller.template_to_video(
            *args,
            **kwargs,
        )

    async def twist_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._controller.twist_to_video(
            *args,
            **kwargs,
        )

    async def addition_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._controller.addition_to_video(
            *args,
            **kwargs,
        )

    async def swap_to_video(
        self,
        *args,
        **kwargs,
    ) -> IPikaResponse:
        return await self._controller.swap_to_video(
            *args,
            **kwargs,
        )

    async def fetch_video_status(
        self,
        *args,
        **kwargs,
    ) -> PikaVideoResponse:
        return await self._controller.fetch_video_status(
            *args,
            **kwargs,
        )
