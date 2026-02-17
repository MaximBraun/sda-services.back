# coding utf-8

from typing import Any

from .core import PikaCelery

from ....domain.repositories import IDatabase

from ...orm.database.models import PikaAccounts

from ...orm.database.repositories import (
    PikaAccountRepository,
    PikaAccountsTokensRepository,
)

from ....interface.schemas.external import (
    PikaAccountData,
    UserToken,
)

from ....interface.schemas.api import AccountBalance


class PikaAccountCelery(PikaCelery):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._account_repository = PikaAccountRepository(
            IDatabase(self._conf),
        )
        self._token_repository = PikaAccountsTokensRepository(
            IDatabase(self._conf),
        )

    async def update_account_record(
        self,
        account: PikaAccounts,
        data: AccountBalance,
    ) -> AccountBalance:
        return await self._account_repository.update_record(
            account.id,
            data=data,
        )

    async def fetch_account_data(
        self,
        account: PikaAccounts,
    ) -> PikaAccountData:
        return await self.client.auth_user(
            account,
        )

    async def fetch_account_balance(
        self,
        token: str,
        api_key: str,
        user_id: str,
    ) -> int:
        return await self.client.fetch_account_credits(
            token,
            api_key,
            user_id,
        )

    async def update_account_balance(
        self,
        account_data: PikaAccountData,
        account: PikaAccounts,
    ) -> Any:
        credits: int = await self.fetch_account_balance(
            account_data.token,
            account_data.api_key,
            account_data.user_id,
        )

        if credits == account.balance:
            return

        is_active: bool = not (credits <= 100 and account.is_active)

        return await self.update_account_record(
            account,
            data=AccountBalance(
                balance=credits,
                is_active=is_active,
            ),
        )

    async def update_account_jwt_token(
        self,
        acc: Any,
        token: str,
    ):
        account_token = await self._token_repository.fetch_with_filters(
            account_id=acc.id
        )
        body = UserToken(account_id=acc.id, jwt_token=token)
        if account_token is not None:
            return await self._token_repository.update_record(
                account_token.id,
                body,
            )
        return await self._token_repository.add_record(
            body,
        )

    async def update_accounts(
        self,
    ) -> Any:
        accounts: list[Any] | None = await self._account_repository.fetch_all()
        for acc in accounts:
            account_data = await self.fetch_account_data(acc)
            await self.update_account_balance(
                account_data,
                acc,
            )
            await self.update_account_jwt_token(
                acc,
                account_data.token,
            )
        return True
