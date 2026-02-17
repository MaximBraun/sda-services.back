# coding utf-8

from ...models import TopmediaAccountsTokens

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class TopmediaAccountTokenRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            TopmediaAccountsTokens,
        )

    async def fetch_token(
        self,
        field_name: str,
        value: str | int,
    ) -> TopmediaAccountsTokens | None:
        data: TopmediaAccountsTokens = await self.fetch_field(
            field_name,
            value,
            many=False,
        )
        if data is not None:
            return data.jwt_token
        return data
