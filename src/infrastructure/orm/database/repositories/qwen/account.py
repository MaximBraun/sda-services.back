# coding utf-8

from ...models import QwenAccounts

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)

from ......domain.entities.qwen import IQwenAccount

from ......domain.errors import TopmediaError


class QwenAccountRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            QwenAccounts,
        )

    async def fetch_account(
        self,
        field_name: str,
        value: str | int,
    ) -> QwenAccounts | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_next_account(
        self,
    ) -> QwenAccounts | None:
        account = await self.fetch_one_with_filter(
            order_by="usage_count",
            is_active=True,
        )
        if account is None:
            raise TopmediaError(
                status_code=503,
            )
        await self.update_record(
            id=account.id,
            data=IQwenAccount(
                usage_count=account.usage_count,
            ),
        )
        return account
