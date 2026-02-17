# coding utf-8

from ......domain.errors.pixverse import PixverseError

from ......infrastructure.orm.database.repositories import (
    UserDataRepository,
)

from ......domain.entities.core import IUserData

from .....schemas.external import (
    UserStatistics,
    UserFilters,
    IPixverseBody,
)


class UserDataController:
    def __init__(
        self,
        repository: UserDataRepository,
    ) -> None:
        self._repository = repository

    async def fetch_user_data(
        self,
        user_id: str | None,
        app_id: str | None,
        app_name: str | None,
        token_data: dict[str, int | str],
    ) -> list[UserStatistics]:
        return await self._repository.fetch_all(
            user_id,
            app_id,
            app_name,
            token_data,
        )

    async def fetch_user_filters(
        self,
        app_name: str | None,
        token_data: dict[str, int | str],
    ) -> UserFilters:
        data: list[UserStatistics] = await self._repository.fetch_all(
            app_name=app_name,
            token_data=token_data,
        )
        return UserFilters(
            user_ids=list({item.user_id for item in data}),
            app_ids=list({item.app_id for item in data}),
        )

    async def fetch_user_tokens(
        self,
        user_id: str,
        app_id: str,
    ) -> IUserData:
        user = await self._repository.fetch_with_filters(
            user_id=str(user_id).strip(),
            app_id=str(app_id).strip(),
        )
        if user is None:
            return IUserData(
                user_id=user_id,
                app_id=app_id,
                balance=0,
            )
        return user
