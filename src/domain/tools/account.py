# coding utf-8

from ..conf import app_conf

from ..entities.core import IConfEnv

from ..repositories import IDatabase

from ...infrastructure.orm.database.repositories import (
    PixverseAccountsTokensRepository,
    TopmediaAccountTokenRepository,
    QwenAccountTokenRepository,
    PikaAccountsTokensRepository,
    WanAccountsTokensRepository,
    XimilarAccountsTokensRepository,
)

from ...infrastructure.orm.database.models import (
    PixverseAccountsTokens,
    TopmediaAccountsTokens,
    QwenAccountsTokens,
    PikaAccountsTokens,
    WanAccountsTokens,
    XimilarAccountsTokens,
)

from ...interface.schemas.external import (
    UserToken,
)

conf: IConfEnv = app_conf()


pixverse_token_repository = PixverseAccountsTokensRepository(
    IDatabase(conf),
)


topmedia_token_repository = TopmediaAccountTokenRepository(
    IDatabase(conf),
)


qwen_token_repository = QwenAccountTokenRepository(
    IDatabase(conf),
)


pika_token_repository = PikaAccountsTokensRepository(
    IDatabase(conf),
)


wan_token_repository = WanAccountsTokensRepository(
    IDatabase(conf),
)


ximilar_token_repository = XimilarAccountsTokensRepository(
    IDatabase(conf),
)


tokens_repository: dict[
    str, TopmediaAccountTokenRepository | PixverseAccountsTokensRepository
] = {
    "pixverse": pixverse_token_repository,
    "topmedia": topmedia_token_repository,
    "qwen": qwen_token_repository,
    "pika": pika_token_repository,
    "wan": wan_token_repository,
    "ximilar": ximilar_token_repository,
}


async def update_account_token(
    account: PixverseAccountsTokens
    | TopmediaAccountsTokens
    | QwenAccountsTokens
    | PikaAccountsTokens
    | WanAccountsTokens
    | XimilarAccountsTokens,
    token: str | None = None,
    api_key: str | None = None,
    user_id: str | None = None,
    cookies: str | None = None,
    project: str = "pixverse",
):
    token_repository = tokens_repository.get(project)

    account_token: (
        PixverseAccountsTokens
        | TopmediaAccountsTokens
        | QwenAccountsTokens
        | PikaAccountsTokens
        | WanAccountsTokens
        | XimilarAccountsTokens,
    ) = await token_repository.fetch_with_filters(
        account_id=account.id,
    )

    body = UserToken(
        account_id=account.id,
        jwt_token=token,
        api_key=api_key,
        user_id=user_id,
        cookies=cookies,
    )

    if account_token is not None:
        return await token_repository.update_record(
            account_token.id,
            body,
        )
    else:
        return await token_repository.add_record(
            body,
        )
