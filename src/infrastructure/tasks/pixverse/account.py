# coding utf-8

from typing import Any

from .core import PixverseCelery

from ....domain.repositories import IDatabase

from ...orm.database.models import PixverseAccounts

from ...orm.database.repositories import (
    PixverseAccountRepository,
    PixverseAccountsTokensRepository,
)

from ....interface.schemas.external import (
    AuthRes,
    TokensResponse,
    UserToken,
)

from ....interface.schemas.api import AccountBalance


class PixverseAccountCelery(PixverseCelery):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._account_repository = PixverseAccountRepository(
            IDatabase(self._conf),
        )
        self._token_repository = PixverseAccountsTokensRepository(
            IDatabase(self._conf),
        )

    async def update_account_record(
        self,
        account: PixverseAccounts,
        data: AccountBalance,
    ) -> AccountBalance:
        return await self._account_repository.update_record(
            account.id,
            data=data,
        )

    async def fetch_account_token(
        self,
        account: PixverseAccounts,
    ) -> AuthRes:
        return await self.client.auth_user(
            account,
        )

    async def fetch_account_balance(
        self,
        token: str,
    ) -> TokensResponse:
        return await self.client.credits_amount(
            token,
        )

    async def update_account_balance(
        self,
        token: AuthRes,
        account: PixverseAccounts,
    ) -> Any:
        balance: TokensResponse = await self.fetch_account_balance(token)

        if balance.credits == account.balance:
            return

        is_active: bool = not (balance.credits <= 100 and account.is_active)

        return await self.update_account_record(
            account,
            data=AccountBalance(
                balance=balance.credits,
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
            token = await self.fetch_account_token(acc)
            await self.update_account_balance(
                token.access_token,
                acc,
            )
            await self.update_account_jwt_token(
                acc,
                token.access_token,
            )
