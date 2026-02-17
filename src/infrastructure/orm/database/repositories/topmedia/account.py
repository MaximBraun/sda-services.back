# coding utf-8

from ...models import TopmediaAccounts

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)

from ......domain.entities.topmedia import IMediatopAccount

from ......domain.errors import TopmediaError


class TopmediaAccountRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            TopmediaAccounts,
        )

    async def fetch_account(
        self,
        field_name: str,
        value: str | int,
    ) -> TopmediaAccounts | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_next_account(
        self,
    ) -> TopmediaAccounts | None:
        account: TopmediaAccounts = await self.fetch_with_filters(
            is_active=True,
        )
        if account is None:
            raise TopmediaError(
                status_code=503,
            )
        await self.update_record(
            id=account.id,
            data=IMediatopAccount(
                usage_count=account.usage_count,
            ),
        )
        return account
