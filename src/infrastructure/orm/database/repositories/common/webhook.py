# coding utf-8

from ...models import Webhooks

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class WebhookRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            Webhooks,
        )

    async def fetch_webhook(
        self,
        field_name: str,
        value: str | int,
    ) -> Webhooks | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )
