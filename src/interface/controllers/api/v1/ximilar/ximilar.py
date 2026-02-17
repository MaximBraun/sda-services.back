# coding utf-8

# from .....schemas.external import (
#     IWanResponse,
#     IWanMediaResponse,
# )

from ......infrastructure.external.ximilar import XimilarClient


class XimilarController:
    def __init__(
        self,
        client: XimilarClient,
    ) -> None:
        self._client = client

    async def image_to_card(
        self,
        *args,
        **kwargs,
    ):
        return await self._client.image_to_card(
            *args,
            **kwargs,
        )
