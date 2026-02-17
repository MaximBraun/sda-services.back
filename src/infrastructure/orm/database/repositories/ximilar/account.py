# coding utf-8

from sqlalchemy import select

from ...models import (
    XimilarAccounts,
    XimilarApplications,
    XimilarAccountApplications,
)

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)

from ......domain.errors import PikaError


class XimilarAccountRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            XimilarAccounts,
        )

    async def fetch_account(
        self,
        field_name: str,
        value: str | int,
    ) -> XimilarAccounts | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_next_account(
        self,
        app_id: str,
    ) -> XimilarAccounts | None:
        stmt = (
            select(XimilarAccounts)
            .join(XimilarAccountApplications)
            .join(XimilarApplications)
            .where(
                XimilarApplications.app_id == app_id,
                XimilarAccounts.is_active.is_(True),
            )
            .order_by(XimilarAccounts.usage_count.asc())
            .limit(1)
        )

        async with self._engine.get_session() as session:
            result = await session.execute(stmt)
            account: XimilarAccounts | None = result.scalars().first()

        if account is None:
            raise PikaError(status_code=25)

        await self.update_record(
            id=account.id,
            data={"usage_count": int(account.usage_count) + 1},
        )
        return account
