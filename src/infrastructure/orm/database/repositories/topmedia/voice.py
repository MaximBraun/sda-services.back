# coding utf-8

from ...models import TopmediaVoices

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class TopmediaVoiceRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            TopmediaVoices,
        )
