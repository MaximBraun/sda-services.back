# coding utf-8

from ...models import WanAccountsTokens

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class WanAccountsTokensRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            WanAccountsTokens,
        )

    async def fetch_token(
        self,
        field_name: str,
        value: str | int,
    ) -> str:
        data: WanAccountsTokens = await self.fetch_field(
            field_name,
            value,
            many=False,
        )
        if data is not None:
            return data.cookies
        return None
