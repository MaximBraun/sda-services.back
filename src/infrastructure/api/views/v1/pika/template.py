# coding utf-8

from ......interface.controllers.api.v1 import PikaTemplateController

from ......interface.schemas.api import (
    Template,
)


class PikaTemplateView:
    def __init__(
        self,
        controller: PikaTemplateController,
    ) -> None:
        self._controller = controller

    async def fetch_templates(
        self,
        token_data: dict[str, int | str],
    ) -> list[Template]:
        return await self._controller.fetch_templates(
            token_data,
        )
