# coding utf-8

from ...models import InstagramSessions

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class InstagramSessionRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            InstagramSessions,
        )

    async def fetch_session(
        self,
        session_id: str,
        many: bool = False,
    ) -> InstagramSessions | None:
        return await self.fetch_field(
            "sessionid",
            session_id,
            many,
        )

    async def fetch_uuid(
        self,
        uuid: str,
        many: bool = False,
    ) -> InstagramSessions | None:
        return await self.fetch_field(
            "uuid",
            uuid,
            many,
        )

    async def fetch_latest_session(
        self,
        user_id: int,
    ):
        return await self.fetch_one_with_filters(
            "user_id",
            user_id,
            "created_at",
        )
