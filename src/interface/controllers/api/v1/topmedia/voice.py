# coding utf-8

from ......infrastructure.orm.database.repositories import TopmediaVoiceRepository

from .....schemas.api import (
    Voice,
)


class TopmediaVoiceController:
    def __init__(
        self,
        repository: TopmediaVoiceRepository,
    ) -> None:
        self._repository = repository

    async def fetch_voices(
        self,
    ) -> list[Voice]:
        return await self._repository.fetch_with_filters(
            many=True,
            is_active=True,
        )
