# coding utf-8

from ......interface.schemas.api import Voice

from ......interface.controllers.api.v1 import TopmediaVoiceController


class TopmediaVoiceView:
    def __init__(
        self,
        controller: TopmediaVoiceController,
    ) -> None:
        self._controller = controller

    async def fetch_voices(
        self,
    ) -> list[Voice]:
        return await self._controller.fetch_voices()
