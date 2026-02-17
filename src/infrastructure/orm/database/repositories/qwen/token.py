# coding utf-8

from ...models import QwenAccountsTokens

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class QwenAccountTokenRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            QwenAccountsTokens,
        )

    async def fetch_token(
        self,
        field_name: str,
        value: str | int,
    ) -> QwenAccountsTokens | None:
        data: QwenAccountsTokens = await self.fetch_field(
            field_name,
            value,
            many=False,
        )
        if data is not None:
            return data.jwt_token
        return data
