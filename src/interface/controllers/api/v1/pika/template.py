# coding utf-8

from ......infrastructure.orm.database.repositories import PikaTemplateRepository

from .....schemas.api import (
    Template,
)


class PikaTemplateController:
    def __init__(
        self,
        repository: PikaTemplateRepository,
    ) -> None:
        self._repository = repository

    async def fetch_templates(
        self,
        token_data: dict[str, int | str],
    ) -> list[Template]:
        return await self._repository.fetch_with_filters(
            many=True,
            auth_user_id=token_data.get("aid"),
        )
