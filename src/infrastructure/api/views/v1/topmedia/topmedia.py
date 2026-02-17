# coding utf-8

from ......domain.entities.topmedia import (
    IT2SBody,
    ITSGBody,
)

from ......interface.schemas.external import TopmediaAPIResponse

from ......interface.controllers.api.v1 import TopmediaController


class TopmediaView:
    def __init__(
        self,
        controller: TopmediaController,
    ) -> None:
        self._controller = controller

    async def text_to_speech(
        self,
        body: IT2SBody,
    ) -> TopmediaAPIResponse:
        return await self._controller.text_to_speech(
            body,
        )

    async def text_to_song(
        self,
        body: ITSGBody,
    ) -> TopmediaAPIResponse:
        return await self._controller.text_to_song(
            body,
        )
