# coding utf-8

from ...models import PikaAccountsTokens

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class PikaAccountsTokensRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PikaAccountsTokens,
        )

    async def fetch_token(
        self,
        field_name: str,
        value: str | int,
    ) -> tuple[str, str, str, str]:
        data: PikaAccountsTokens = await self.fetch_field(
            field_name,
            value,
            many=False,
        )
        if data is not None:
            return (
                data.jwt_token,
                data.api_key,
                data.user_id,
                data.cookies,
            )
        return (
            None,
            None,
            None,
            None,
        )
