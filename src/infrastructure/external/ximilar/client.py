# coding utf-8

from asyncio import sleep

from os import getenv

from fastapi import UploadFile

from .core import XimilarCore

from ....domain.conf import app_conf

from ....domain.errors import WanError

from ....domain.repositories import IDatabase

from ....domain.typing.enums import (
    XimilarEndpoint,
    XimilarMethod,
)

from ....domain.tools import (
    update_account_token,
)

from ....domain.entities.core import (
    IConfEnv,
)

from ....domain.entities.ximilar import (
    XimilarAuthBody,
    XimilarAuthResponse,
    XimilarCardBody,
    CardResponse,
)

from ...orm.database.repositories import (
    UserDataRepository,
    XimilarAccountRepository,
    XimilarAccountsTokensRepository,
    UserGenerationRepository,
)

from ...orm.database.models import XimilarAccounts

from ....interface.schemas.external import (
    GenerationData,
    UsrData,
)


conf: IConfEnv = app_conf()


ximilar_account_database = XimilarAccountRepository(
    engine=IDatabase(conf),
)


ximilar_account_token_database = XimilarAccountsTokensRepository(
    engine=IDatabase(conf),
)


user_generations_database = UserGenerationRepository(
    engine=IDatabase(conf),
)

user_data_database = UserDataRepository(
    engine=IDatabase(conf),
)


class XimilarClient:
    def __init__(
        self,
        core: XimilarCore,
    ) -> None:
        self._core = core

    async def auth_user(
        self,
        account: XimilarAccounts,
    ) -> str:
        response = await self._core.post(
            url_method=XimilarMethod.API,
            endpoint=XimilarEndpoint.AUTH,
            body=XimilarAuthBody(
                username=account.username,
                password=account.password,
            ),
        )

        data = XimilarAuthResponse(**response)

        return data.access

    async def __fetch_account_token(
        self,
        account: XimilarAccounts,
    ) -> str:
        token: str | None = await ximilar_account_token_database.fetch_token(
            "account_id",
            account.id,
        )
        if token is None:
            token: str = await self.auth_user(account)

            await update_account_token(
                account,
                project="ximilar",
                token=token,
            )

        return token

    async def __handle_success(
        self,
        data: CardResponse,
        account_id: int,
        user_id: str,
        app_id: str,
    ):
        # await user_generations_database.add_record(
        #     GenerationData(
        #         generation_id=data.data,
        #         account_id=account_id,
        #         user_id=user_id,
        #         app_id=app_id,
        #         app_name=getenv("APP_SERVICE", "ximilar").lower(),
        #     )
        # )
        # await user_data_database.create_or_update_user_data(
        #     UsrData(
        #         user_id=user_id,
        #         app_id=app_id,
        #     )
        # )
        return data

    async def __handle_failure(
        self,
        status_code: int,
        extra: dict[str] = {},
    ) -> WanError:
        error = WanError(
            status_code=9999 if status_code is None else status_code,
            extra=extra,
        )

        raise error

    async def __reauthenticate(
        self,
        account: XimilarAccounts,
    ) -> str:
        return await self.auth_user(
            account,
        )

    async def __generate_image(
        self,
        image: UploadFile,
    ) -> XimilarCardBody:
        return await XimilarCardBody.from_upload(
            image,
        )

    async def image_to_card(
        self,
        image: UploadFile,
        user_id: str,
        app_id: str,
    ) -> CardResponse:
        account: (
            XimilarAccounts | None
        ) = await ximilar_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise WanError(status_code=5005)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            account_token: str = await self.__fetch_account_token(
                account,
            )
            try:

                async def call(
                    token: str,
                    image: UploadFile,
                ):
                    body: XimilarCardBody = await self.__generate_image(
                        image=image,
                    )

                    data = await self._core.post(
                        token=token,
                        url_method=XimilarMethod.API,
                        endpoint=XimilarEndpoint.CARD,
                        body=body,
                    )

                    return CardResponse.from_full_response(data)

                data: CardResponse = await call(
                    account_token,
                    image,
                )

                # if data.error_code == 0:
                return await self.__handle_success(
                    data,
                    account_id,
                    user_id,
                    app_id,
                )

                # elif data.error_code == 4009:
                #     raise WanError(data.error_code)

                # last_err_code = data.error_code

            except Exception:
                if attempt == max_attempts - 1:
                    account_token: str = await self.__reauthenticate(
                        account,
                    )

                    await update_account_token(
                        account,
                        token=account_token,
                        project="ximilar",
                    )

                    try:
                        data: CardResponse = await call(
                            account_token,
                            image,
                        )

                        # if data.error_code == 0:
                        return await self.__handle_success(
                            data,
                            account_id,
                            user_id,
                            app_id,
                        )
                    except Exception as final_err:
                        raise final_err
                    # return await self.__handle_failure(data.error_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )
