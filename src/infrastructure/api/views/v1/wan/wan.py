# # coding utf-8

from ......interface.controllers.api.v1 import WanController

from ......interface.schemas.external import (
    IWanResponse,
    IWanMediaResponse,
)


class WanView:
    def __init__(
        self,
        controller: WanController,
    ) -> None:
        self._controller = controller

    async def text_to_image(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._controller.text_to_image(
            *args,
            **kwargs,
        )

    async def photo_to_photo(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._controller.photo_to_photo(
            *args,
            **kwargs,
        )

    async def template_to_photo(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._controller.template_to_photo(
            *args,
            **kwargs,
        )

    async def template_to_avatar(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._controller.template_to_avatar(
            *args,
            **kwargs,
        )

    async def text_to_video(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._controller.text_to_video(
            *args,
            **kwargs,
        )

    async def image_to_video(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._controller.image_to_video(
            *args,
            **kwargs,
        )

    async def template_to_video(
        self,
        *args,
        **kwargs,
    ) -> IWanResponse:
        return await self._controller.template_to_video(
            *args,
            **kwargs,
        )

    async def fetch_media_status(
        self,
        *args,
        **kwargs,
    ) -> IWanMediaResponse:
        return await self._controller.fetch_media_status(
            *args,
            **kwargs,
        )
