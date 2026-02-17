# coding utf-8

from ......domain.entities.topmedia import IT2SBody, ITSGBody

from ......interface.schemas.external import TopmediaAPIResponse

from ......infrastructure.external.topmedia import TopmediaClient


class TopmediaController:
    def __init__(
        self,
        client: TopmediaClient,
    ) -> None:
        self._client = client

    async def text_to_speech(
        self,
        body: IT2SBody,
    ) -> TopmediaAPIResponse:
        return await self._client.text_to_speech(
            body,
        )

    async def text_to_song(
        self,
        body: ITSGBody,
    ) -> TopmediaAPIResponse:
        return await self._client.text_to_song(
            body,
        )
