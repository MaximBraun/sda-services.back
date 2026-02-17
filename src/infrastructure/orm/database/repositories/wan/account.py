# coding utf-8

from sqlalchemy import select

from ...models import (
    WanAccounts,
    WanApplications,
    WanAccountApplications,
)

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)

from ......domain.errors import PikaError


class WanAccountRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            WanAccounts,
        )

    async def fetch_account(
        self,
        field_name: str,
        value: str | int,
    ) -> WanAccounts | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_next_account(
        self,
        app_id: str,
    ) -> WanAccounts | None:
        stmt = (
            select(WanAccounts)
            .join(WanAccountApplications)
            .join(WanApplications)
            .where(
                WanApplications.app_id == app_id,
                WanAccounts.is_active.is_(True),
            )
            .order_by(WanAccounts.usage_count.asc())
            .limit(1)
        )

        async with self._engine.get_session() as session:
            result = await session.execute(stmt)
            account: WanAccounts | None = result.scalars().first()

        if account is None:
            raise PikaError(status_code=25)

        await self.update_record(
            id=account.id,
            data={"usage_count": int(account.usage_count) + 1},
        )
        return account
