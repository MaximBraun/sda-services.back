# coding utf-8

from collections import defaultdict

from sqlalchemy import select, and_

from ...models import (
    UserData,
    UserGenerations,
    PixverseAccounts,
)

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)

from ......interface.schemas.external import (
    UsrData,
    AccountInfo,
    UserStatistics,
    UserUpdateData,
)


class UserDataRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            UserData,
        )

    async def create_or_update_user_data(
        self,
        body: UserUpdateData,
    ):
        user_data: UserUpdateData = await self.fetch_with_filters(
            user_id=body.user_id,
            app_id=body.app_id,
        )
        if user_data is not None:
            return await self.update_record(
                user_data.id,
                data=UserUpdateData(
                    user_id=body.user_id,
                    app_id=body.app_id,
                    balance=body.balance
                    if isinstance(body, UserUpdateData)
                    else user_data.balance,
                    app_id_usage=int(1 + user_data.app_id_usage),
                ),
            )
        return await self.add_record(body)

    async def fetch_all(
        self,
        user_id: str | None = None,
        app_id: str | None = None,
        app_name: str | None = None,
        token_data: dict[str, int | str] = None,
    ) -> list[UserStatistics]:
        stmt = (
            select(
                UserData.id,
                UserData.user_id,
                UserData.app_id,
                UserData.balance,
                UserData.app_id_usage,
                UserGenerations.generation_id,
                UserGenerations.generation_url,
                PixverseAccounts.id.label("account_id"),
                PixverseAccounts.username,
            )
            .outerjoin(
                UserGenerations,
                (UserData.user_id == UserGenerations.user_id)
                & (UserData.app_id == UserGenerations.app_id),
            )
            .outerjoin(
                PixverseAccounts,
                UserGenerations.account_id == PixverseAccounts.id,
            )
        )

        filters = []
        if user_id is not None:
            filters.append(UserData.user_id == user_id)
        if app_id is not None:
            filters.append(UserData.app_id == app_id)
        if app_name is not None:
            filters.append(UserGenerations.app_name == app_name)

        # фильтрация по auth_user_id
        if token_data and (aid := token_data.get("aid")) is not None:
            filters.append(PixverseAccounts.auth_user_id == aid)

        if filters:
            stmt = stmt.where(and_(*filters))

        async with self._engine.get_session() as session:
            rows = (await session.execute(stmt)).all()

        grouped = defaultdict(lambda: {"generations": set(), "accounts": {}})
        output = []

        for row in rows:
            uid = row.id
            generation_value = row.generation_id or row.generation_url
            if generation_value:
                grouped[uid]["generations"].add(generation_value)
            if row.account_id:
                grouped[uid]["accounts"][row.account_id] = row.username

        for row in rows:
            uid = row.id
            if any(s.id == uid for s in output):
                continue
            output.append(
                UserStatistics(
                    id=uid,
                    user_id=row.user_id,
                    app_id=row.app_id,
                    balance=row.balance,
                    app_id_usage=row.app_id_usage,
                    generation_ids=sorted(map(str, grouped[uid]["generations"])),
                    accounts=[
                        AccountInfo(id=aid, username=uname)
                        for aid, uname in grouped[uid]["accounts"].items()
                    ],
                )
            )

        return output
