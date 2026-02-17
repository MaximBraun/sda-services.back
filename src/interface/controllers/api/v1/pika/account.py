# coding utf-8

from ......infrastructure.orm.database.repositories import PikaAccountRepository

from .....schemas.api import (
    Account,
)


class PikaAccountController:
    def __init__(
        self,
        repository: PikaAccountRepository,
    ) -> None:
        self._repository = repository

    async def fetch_accounts(
        self,
        token_data: dict[str, str | int],
    ) -> list[Account]:
        return await self._repository.fetch_with_filters(
            many=True,
            auth_user_id=token_data.get("aid"),
        )
