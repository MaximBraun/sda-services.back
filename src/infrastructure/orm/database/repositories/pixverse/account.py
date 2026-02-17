# coding utf-8

from sqlalchemy import select

from ...models import (
    PixverseAccounts,
    PixverseApplications,
    PixverseAccountApplications,
)

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)

from ......domain.errors import PixverseError


class PixverseAccountRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PixverseAccounts,
        )

    async def fetch_account(
        self,
        field_name: str,
        value: str | int,
    ) -> PixverseAccounts | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_next_account(
        self,
        app_id: str,
    ) -> PixverseAccounts | None:
        stmt = (
            select(PixverseAccounts)
            .join(PixverseAccountApplications)
            .join(PixverseApplications)
            .where(
                PixverseApplications.app_id == app_id,
                PixverseAccounts.is_active.is_(True),
            )
            .order_by(PixverseAccounts.usage_count.asc())
            .limit(1)
        )

        async with self._engine.get_session() as session:
            result = await session.execute(stmt)
            account: PixverseAccounts | None = result.scalars().first()

        if account is None:
            raise PixverseError(status_code=985)

        # обновляем usage_count
        await self.update_record(
            id=account.id,
            data={"usage_count": int(account.usage_count) + 1},
        )
        return account
