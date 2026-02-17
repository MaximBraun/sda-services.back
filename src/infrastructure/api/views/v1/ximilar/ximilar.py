# # coding utf-8

from ......interface.controllers.api.v1 import XimilarController

# from ......interface.schemas.external import (
#     IWanResponse,
#     IWanMediaResponse,
# )


class XimilarView:
    def __init__(
        self,
        controller: XimilarController,
    ) -> None:
        self._controller = controller

    async def image_to_card(
        self,
        *args,
        **kwargs,
    ):
        return await self._controller.image_to_card(
            *args,
            **kwargs,
        )
