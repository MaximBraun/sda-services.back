# coding utf-8

from typing import Any

from .core import InstagramCelery

from ....domain.repositories import IDatabase

from ...orm.database.models import InstagramSessions

from ...orm.database.repositories import (
    InstagramSessionRepository,
)


class InstagramSessionCelery(InstagramCelery):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._session_repository = InstagramSessionRepository(
            IDatabase(self._conf),
        )

    async def __fetch_sessions(
        self,
    ):
        user_sessions: (
            list[InstagramSessions] | None
        ) = await self._session_repository.fetch_all()

        latest: dict[tuple[str, int], Any] = {}

        for session in user_sessions:
            key = (session.ds_user_id, session.user_id)
            if key not in latest or session.created_at > latest[key].created_at:
                latest[key] = session

        return list(latest.values())

    async def update_sessions_data(
        self,
    ) -> Any:
        user_sessions: list[InstagramSessions] | None = await self.__fetch_sessions()
        for session in user_sessions:
            try:
                await self.client.update_user_data(
                    body=None,
                    uuid=session.uuid,
                )
            except Exception as err:
                pass
        return True
