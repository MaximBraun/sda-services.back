# coding utf-8

from ...models import PixverseAccountsTokens

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class PixverseAccountsTokensRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PixverseAccountsTokens,
        )

    async def fetch_token(
        self,
        field_name: str,
        value: str | int,
    ) -> PixverseAccountsTokens | None:
        data = await self.fetch_field(
            field_name,
            value,
            many=False,
        )
        if data is not None:
            return data.jwt_token
        return data
