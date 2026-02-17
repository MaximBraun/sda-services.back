# coding utf-8

from asyncio import sleep

from os import (
    getenv,
    path,
)

from io import BytesIO

from fastapi import UploadFile

from .core import (
    PikaCore,
    PikaSessionCore,
)

from json import loads

from ....domain.conf import app_conf

from ....domain.errors import PikaError

from ....domain.repositories import IDatabase

from ....domain.typing.enums import (
    PikaEndpoint,
    PikaMethod,
)

from ....domain.tools import (
    update_account_token,
)

from ....domain.entities.core import (
    IConfEnv,
)

from ....domain.entities.pika import (
    IT2VBody,
    IV2TBody,
    IP2VBody,
    IV2VBody,
    II2GBody,
    IV2SBody,
    II2VBody,
)

from ...orm.database.repositories import (
    UserDataRepository,
    PikaAccountRepository,
    PikaAccountsTokensRepository,
    UserGenerationRepository,
)

from ...orm.database.models import (
    PikaAccounts,
    UserGenerations,
)


from ....interface.schemas.external import (
    PikaResponse,
    UserCredentials,
    PikaCreditResponse,
    PikaGenerationResponse,
    PikaVideoResponse,
    IPikaResponse,
    PikaAccountData,
    GenerationData,
    UsrData,
    PikaT2VBody,
    PikaV2VBody,
    IMediaFileData,
)


conf: IConfEnv = app_conf()


pika_account_database = PikaAccountRepository(
    engine=IDatabase(conf),
)


pika_account_token_database = PikaAccountsTokensRepository(
    engine=IDatabase(conf),
)


user_generations_database = UserGenerationRepository(
    engine=IDatabase(conf),
)

user_data_database = UserDataRepository(
    engine=IDatabase(conf),
)


class PikaClient:
    def __init__(
        self,
        core: PikaCore,
        session: PikaSessionCore,
    ) -> None:
        self._core = core
        self._session = session

    async def auth_user(
        self,
        account: PikaAccounts,
    ) -> PikaAccountData:
        max_attempts = 10

        for attempt in range(max_attempts):
            try:
                return await self._session.fetch_auth_token(
                    credentials=UserCredentials(
                        username=account.username,
                        password=account.password,
                    )
                )
            except Exception:
                await sleep(1)
        raise RuntimeError("Canno't auth current account")

    async def __handle_success(
        self,
        data: PikaGenerationResponse,
        account_id: int,
        user_id: str,
        app_id: str,
    ) -> IPikaResponse:
        await user_generations_database.add_record(
            GenerationData(
                generation_id=data.data.id,
                account_id=account_id,
                user_id=user_id,
                app_id=app_id,
                app_name=getenv("APP_SERVICE", "pika").lower(),
            )
        )
        await user_data_database.create_or_update_user_data(
            UsrData(
                user_id=user_id,
                app_id=app_id,
            )
        )
        return IPikaResponse(
            video_id=data.data.id,
        )

    async def __handle_failure(
        self,
        status_code: int,
        extra: dict[str] = {},
    ) -> PikaError:
        error = PikaError(
            status_code=999 if status_code is None else status_code,
            extra=extra,
        )

        raise error

    def __fetch_ext(
        self,
        file: UploadFile,
    ) -> str:
        return path.splitext(file.filename)[-1].lower().lstrip(".")

    async def __pick_file(
        self,
        files: list[UploadFile] | UploadFile,
        prefix: str | tuple[str, ...],
    ) -> IMediaFileData | None:
        fs = files if isinstance(files, list) else [files]
        file = next((f for f in fs if f.content_type.startswith(prefix)), None)
        return IMediaFileData(
            bytes=await file.read(),
            ext=self.__fetch_ext(file),
        )

    async def __get_account_data(
        self,
        account: PikaAccounts,
    ) -> PikaAccountData:
        (
            token,
            api_key,
            user_id,
            cookies,
        ) = await pika_account_token_database.fetch_token(
            "account_id",
            account.id,
        )
        if token is None:
            token, api_key, user_id, cookies = await self.auth_user(
                account,
            )

            await update_account_token(
                account,
                token,
                api_key=api_key,
                user_id=user_id,
                cookies=cookies,
                project="pika",
            )

        return PikaAccountData(
            token=token,
            api_key=api_key,
            user_id=user_id,
            cookies=cookies,
        )

    async def __reauthenticate(
        self,
        account,
    ) -> PikaAccountData:
        return await self.auth_user(
            account,
        )

    async def fetch_account_credits(
        self,
        token: str,
        api_key: str,
        user_id: str,
    ) -> int:
        data: PikaCreditResponse = await self._core.get(
            token=token,
            api_key=api_key,
            url_method=PikaMethod.LOGIN,
            endpoint=PikaEndpoint.BALANCE.format(
                user_id=user_id,
            ),
        )

        if isinstance(data, PikaResponse) and data.message == "Unauthorized":
            raise PikaError(status_code=8)

        return data.credits

    async def text_to_video(
        self,
        body: PikaT2VBody,
        user_id: str,
        app_id: str,
    ) -> IPikaResponse:
        account: PikaAccounts | None = await pika_account_database.fetch_next_account(
            app_id,
        )

        if account is None:
            raise PikaError(status_code=55)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            account_data: PikaAccountData = await self.__get_account_data(
                account,
            )
            try:

                async def call(
                    account_data: PikaAccountData,
                ) -> PikaGenerationResponse | PikaResponse:
                    return await self._core.post(
                        token=account_data.token,
                        url_method=PikaMethod.GENEREATE,
                        endpoint=PikaEndpoint.V2,
                        data=IT2VBody(
                            prompt=body.prompt,
                            user_id=account_data.user_id,
                        ),
                    )

                data: PikaGenerationResponse | PikaResponse = await call(
                    account_data,
                )

                if isinstance(data, PikaResponse) and data.message == "Unauthorized":
                    raise PikaError(status_code=8)

                elif data.success is True:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                last_err_code = data.code

            except Exception:
                if attempt == max_attempts - 1:
                    account_data = await self.__reauthenticate(
                        account,
                    )

                    await update_account_token(
                        account,
                        **account_data.dict,
                        project="pika",
                    )

                    try:
                        data = await call(
                            account_data,
                        )

                        if not isinstance(data, PikaResponse):
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error)
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

    async def image_to_video(
        self,
        body: PikaT2VBody,
        image: UploadFile,
        user_id: str,
        app_id: str,
    ) -> IPikaResponse:
        account: PikaAccounts | None = await pika_account_database.fetch_next_account(
            app_id,
        )

        image_data = await self.__pick_file(
            image,
            "image/",
        )

        if account is None:
            raise PikaError(status_code=55)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            account_data: PikaAccountData = await self.__get_account_data(
                account,
            )
            try:

                async def call(
                    account_data: PikaAccountData,
                ) -> PikaGenerationResponse | PikaResponse:
                    return await self._core.post(
                        token=account_data.token,
                        url_method=PikaMethod.GENEREATE,
                        endpoint=PikaEndpoint.V1,
                        data=IP2VBody(
                            prompt=body.prompt,
                            user_id=account_data.user_id,
                        ),
                        files={
                            "image": (
                                image_data.filename,
                                BytesIO(image_data.bytes),
                                "image/jpeg",
                            ),
                        },
                    )

                data: PikaGenerationResponse | PikaResponse = await call(
                    account_data,
                )

                if isinstance(data, PikaResponse) and data.message == "Unauthorized":
                    raise PikaError(status_code=8)

                elif data.success is True:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                last_err_code = data.code

            except Exception:
                if attempt == max_attempts - 1:
                    account_data = await self.__reauthenticate(
                        account,
                    )

                    await update_account_token(
                        account,
                        **account_data.dict,
                        project="pika",
                    )

                    try:
                        data = await call(
                            account_data,
                        )

                        if not isinstance(data, PikaResponse):
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error)
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

    async def template_to_video(
        self,
        body: PikaV2VBody,
        image: UploadFile,
        user_id: str,
        app_id: str,
    ) -> IPikaResponse:
        account: PikaAccounts | None = await pika_account_database.fetch_next_account(
            app_id,
        )

        image_data = await self.__pick_file(
            image,
            "image/",
        )

        if account is None:
            raise PikaError(status_code=55)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            account_data: PikaAccountData = await self.__get_account_data(
                account,
            )
            try:

                async def call(
                    account_data: PikaAccountData,
                ) -> PikaGenerationResponse | PikaResponse:
                    return await self._core.post(
                        token=account_data.token,
                        url_method=PikaMethod.GENEREATE,
                        endpoint=PikaEndpoint.EFFECTS,
                        data=II2VBody(
                            pika_ffect=body.template_id,
                            user_id=account_data.user_id,
                        ),
                        files={
                            "image": (
                                image_data.filename,
                                BytesIO(image_data.bytes),
                                "image/jpeg",
                            )
                        },
                    )

                data: PikaGenerationResponse | PikaResponse = await call(
                    account_data,
                )

                if isinstance(data, PikaResponse) and data.message == "Unauthorized":
                    raise PikaError(status_code=8)

                elif data.success is True:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                last_err_code = data.code

            except Exception:
                if attempt == max_attempts - 1:
                    account_data = await self.__reauthenticate(
                        account,
                    )

                    await update_account_token(
                        account,
                        **account_data.dict,
                        project="pika",
                    )

                    try:
                        data = await call(
                            account_data,
                        )

                        if not isinstance(data, PikaResponse):
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error)
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

    async def twist_to_video(
        self,
        body: PikaT2VBody,
        video: UploadFile,
        user_id: str,
        app_id: str,
    ) -> IPikaResponse:
        account: PikaAccounts | None = await pika_account_database.fetch_next_account(
            app_id,
        )

        video_data = await self.__pick_file(
            video,
            "video/",
        )

        if account is None:
            raise PikaError(status_code=55)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            account_data: PikaAccountData = await self.__get_account_data(
                account,
            )
            try:

                async def call(
                    account_data: PikaAccountData,
                ) -> PikaGenerationResponse | PikaResponse:
                    return await self._core.post(
                        token=account_data.token,
                        url_method=PikaMethod.GENEREATE,
                        endpoint=PikaEndpoint.V2,
                        data=IV2TBody(
                            prompt=body.prompt,
                            user_id=account_data.user_id,
                        ),
                        files={
                            "video": (
                                video_data.filename,
                                BytesIO(video_data.bytes),
                                "video/mp4",
                            )
                        },
                    )

                data: PikaGenerationResponse | PikaResponse = await call(
                    account_data,
                )

                if isinstance(data, PikaResponse) and data.message == "Unauthorized":
                    raise PikaError(status_code=8)

                elif data.success is True:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                last_err_code = data.code

            except Exception:
                if attempt == max_attempts - 1:
                    account_data = await self.__reauthenticate(
                        account,
                    )

                    await update_account_token(
                        account,
                        **account_data.dict,
                        project="pika",
                    )

                    try:
                        data = await call(
                            account_data,
                        )

                        if not isinstance(data, PikaResponse):
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error)
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

    async def addition_to_video(
        self,
        body: PikaT2VBody,
        files: list[UploadFile],
        user_id: str,
        app_id: str,
    ) -> IPikaResponse:
        account: PikaAccounts | None = await pika_account_database.fetch_next_account(
            app_id,
        )

        video_data = await self.__pick_file(
            files,
            "video/",
        )

        image_data = await self.__pick_file(
            files,
            "image/",
        )

        if account is None:
            raise PikaError(status_code=55)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            account_data: PikaAccountData = await self.__get_account_data(
                account,
            )
            try:

                async def call(
                    account_data: PikaAccountData,
                ) -> PikaGenerationResponse | PikaResponse:
                    return await self._core.post(
                        token=account_data.token,
                        url_method=PikaMethod.GENEREATE,
                        endpoint=PikaEndpoint.V2,
                        data=IV2VBody(
                            prompt=body.prompt,
                            user_id=account_data.user_id,
                        ),
                        files={
                            "video": (
                                video_data.filename,
                                BytesIO(video_data.bytes),
                                "video/mp4",
                            ),
                            "image": (
                                image_data.filename,
                                BytesIO(image_data.bytes),
                                "image/jpeg",
                            ),
                        },
                    )

                data: PikaGenerationResponse | PikaResponse = await call(
                    account_data,
                )

                if isinstance(data, PikaResponse) and data.message == "Unauthorized":
                    raise PikaError(status_code=8)

                elif data.success is True:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                last_err_code = data.code

            except Exception:
                if attempt == max_attempts - 1:
                    account_data = await self.__reauthenticate(
                        account,
                    )

                    await update_account_token(
                        account,
                        **account_data.dict,
                        project="pika",
                    )

                    try:
                        data = await call(
                            account_data,
                        )

                        if not isinstance(data, PikaResponse):
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error)
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

    async def swap_to_video(
        self,
        files: list[UploadFile],
        user_id: str,
        app_id: str,
    ) -> IPikaResponse:
        account: PikaAccounts | None = await pika_account_database.fetch_next_account(
            app_id,
        )

        video_data = await self.__pick_file(
            files,
            "video/",
        )

        image_data = await self.__pick_file(
            files,
            "image/",
        )

        if account is None:
            raise PikaError(status_code=55)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            account_data: PikaAccountData = await self.__get_account_data(
                account,
            )
            try:

                async def call(
                    account_data: PikaAccountData,
                ) -> PikaGenerationResponse | PikaResponse:
                    return await self._core.post(
                        token=account_data.token,
                        url_method=PikaMethod.GENEREATE,
                        endpoint=PikaEndpoint.V2,
                        data=IV2SBody(
                            user_id=account_data.user_id,
                        ),
                        files={
                            "video": (
                                video_data.filename,
                                BytesIO(video_data.bytes),
                                "video/mp4",
                            ),
                            "image": (
                                image_data.filename,
                                BytesIO(image_data.bytes),
                                "image/jpeg",
                            ),
                        },
                    )

                data: PikaGenerationResponse | PikaResponse = await call(
                    account_data,
                )

                if isinstance(data, PikaResponse) and data.message == "Unauthorized":
                    raise PikaError(status_code=8)

                elif data.success is True:
                    return await self.__handle_success(
                        data,
                        account_id,
                        user_id,
                        app_id,
                    )

                last_err_code = data.code

            except Exception:
                if attempt == max_attempts - 1:
                    # account_data = await self.__reauthenticate(
                    #     account,
                    # )

                    # await update_account_token(
                    #     account,
                    #     **account_data.dict,
                    #     project="pika",
                    # )

                    account_data = await self.__get_account_data(
                        account,
                    )

                    try:
                        data = await call(
                            account_data,
                        )

                        if not isinstance(data, PikaResponse):
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error)
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

    async def fetch_video_status(
        self,
        id: str,
    ) -> PikaVideoResponse:
        generation_data: (
            UserGenerations | None
        ) = await user_generations_database.fetch_generation(
            "generation_id",
            id,
        )

        if generation_data is None:
            raise PikaError(status_code=35)

        account: PikaAccounts | None = await pika_account_database.fetch_account(
            "id",
            generation_data.account_id,
        )

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            account_data = await self.__get_account_data(
                account,
            )
            try:

                async def call(
                    account_data: PikaAccountData,
                    id: str,
                ) -> PikaVideoResponse:
                    data: bytes = await self._core.post(
                        cookie=account_data.cookies,
                        is_serialized=False,
                        url_method=PikaMethod.BASE,
                        endpoint=PikaEndpoint.STATUS,
                        body=[II2GBody(ids=[id])],
                    )

                    decoded: str = data.decode()

                    str_data: str = next(
                        line[2:]
                        for line in decoded.splitlines()
                        if line.startswith("1:")
                    )

                    return PikaVideoResponse.from_data(
                        loads(str_data),
                    )

                data: PikaVideoResponse | PikaResponse = await call(
                    account_data.cookies,
                    id,
                )

                if isinstance(data, PikaResponse) and data.message == "Unauthorized":
                    raise PikaError(status_code=8)

                return data

            except Exception:
                if attempt == max_attempts - 1:
                    # account_data = await self.__reauthenticate(
                    #     account,
                    # )

                    # await update_account_token(
                    #     account,
                    #     **account_data.dict,
                    #     project="pika",
                    # )

                    account_data = await self.__get_account_data(
                        account,
                    )

                    try:
                        data = await call(
                            account_data,
                            id,
                        )

                        if not isinstance(data, PikaResponse):
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.error)
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
