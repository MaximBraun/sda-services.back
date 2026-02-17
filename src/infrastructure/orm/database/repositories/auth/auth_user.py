# coding utf-8

from ...models import AuthUsers

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class AuthUserRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            AuthUsers,
        )

    async def fetch_user(
        self,
        field_name: str,
        value: str,
    ) -> AuthUsers | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )
