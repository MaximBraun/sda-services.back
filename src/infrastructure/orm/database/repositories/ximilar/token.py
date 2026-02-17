# coding utf-8

from ...models import XimilarAccountsTokens

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class XimilarAccountsTokensRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            XimilarAccountsTokens,
        )

    async def fetch_token(
        self,
        field_name: str,
        value: str | int,
    ) -> XimilarAccountsTokens | None:
        data = await self.fetch_field(
            field_name,
            value,
            many=False,
        )
        if data is not None:
            return data.jwt_token
        return data
