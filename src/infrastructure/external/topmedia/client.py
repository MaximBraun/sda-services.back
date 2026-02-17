# coding utf-8

from .core import TopmediaCore

from asyncio import sleep

from ....domain.conf import app_conf

from ....domain.errors import TopmediaError

from ....domain.typing.enums import (
    TopmediaEndpoint,
    TopmediaMethod,
    AccountProjectToken,
)

from ....domain.entities.core import (
    IConfEnv,
)

from ....domain.entities.topmedia import (
    IT2SBody,
    ITSGBody,
    TextSlangBody,
    TextSpeechBody,
    TextMusicBody,
    TopmediaLoginParams,
    TopmediaTokenParams,
    TopmediaMusicParams,
)

from ...orm.database.models import (
    TopmediaAccounts,
    TopmediaAccountsTokens,
)

from ...orm.database.repositories import (
    TopmediaAccountTokenRepository,
    TopmediaAccountRepository,
)

from ....domain.repositories import IDatabase

from ....domain.tools import update_account_token

from ....interface.schemas.external import (
    TopmediaResponse,
    TopmediaTokenData,
    TopmediaSlangData,
    TopmediaSpeechData,
    TopmediaSongData,
    TopmediaSpeechResponse,
    TopmediaMusicResponse,
    TopmediaSongResponse,
    TopmediaAPIResponse,
    TopmediaAPIResponseData,
)


conf: IConfEnv = app_conf()


account_database = TopmediaAccountRepository(
    engine=IDatabase(conf),
)


account_token_database = TopmediaAccountTokenRepository(
    engine=IDatabase(conf),
)


class TopmediaClient:
    """Клиентский интерфейс для работы с PixVerse API.

    Предоставляет удобные методы для основных операций с видео контентом:
    - Генерация видео из текста
    - Создание видео из изображений
    - Проверка статуса задач

    Args:
        core (PixVerseCore): Базовый клиент для выполнения запросов
    """

    def __init__(
        self,
        core: TopmediaCore,
    ) -> None:
        self._core = core

    async def auth_user_account(
        self,
        account: TopmediaAccounts,
    ) -> str:
        data: TopmediaResponse = await self._core.post(
            # Request **kwargs
            url_method=TopmediaMethod.AUTH,
            endpoint=TopmediaEndpoint.AUTH,
            params=TopmediaLoginParams(
                email=account.username,
                password=account.password,
            ),
        )
        if data.code != 200:
            error = TopmediaError(
                status_code=data.code,
            )

            raise error
        return data.resp.access_token

    async def __handle_failure(
        self,
        status_code: int,
        extra: dict[str] = {},
    ) -> TopmediaError:
        error = TopmediaError(
            status_code=status_code if status_code is not None else 505,
            extra=extra,
        )

        raise error

    async def __get_account_token(
        self,
        account: TopmediaAccounts,
    ) -> str:
        token_data: TopmediaAccountsTokens = (
            await account_token_database.fetch_with_filters(
                account_id=account.id,
            )
        )

        token = token_data.jwt_token

        if token is None:
            token: str = await self.auth_user_account(account)

            await update_account_token(
                account,
                token,
                project=AccountProjectToken.TOPMEDIA,
            )

        return token

    async def __reauthenticate(
        self,
        account: TopmediaAccounts,
    ) -> str:
        return await self.auth_user_account(
            account,
        )

    async def __fetch_token_status(
        self,
        token: str,
    ) -> TopmediaTokenData:
        data: TopmediaResponse = await self._core.get(
            token=token,
            # Request **kwargs
            url_method=TopmediaMethod.VOICE,
            endpoint=TopmediaEndpoint.USER,
            params=TopmediaTokenParams(
                token=token,
            ),
        )

        if data.status != 200:
            raise TopmediaError(data.status)

        return data.resp

    async def __fetch_slang_text_status(
        self,
        token: str,
        body: IT2SBody,
    ) -> TopmediaSlangData:
        data: TopmediaResponse = await self._core.post(
            token=token,
            # Request **kwargs
            url_method=TopmediaMethod.VOICE,
            endpoint=TopmediaEndpoint.SLANG,
            body=TextSlangBody(
                **body.dict,
                token=token,
            ),
        )

        if data.status != 200:
            raise TopmediaError(data.status)

        return data.resp

    async def __generate_text_speech(
        self,
        token: str,
        body: IT2SBody,
    ) -> TopmediaSpeechData:
        data: TopmediaResponse = await self._core.post(
            token=token,
            # Request **kwargs
            url_method=TopmediaMethod.VOICE,
            endpoint=TopmediaEndpoint.SPEECH,
            data=TextSpeechBody(
                **body.dict,
                token=token,
            ),
        )

        if data.status != 200:
            raise TopmediaError(data.status)

        return data.resp

    async def __generate_text_song(
        self,
        token: str,
        body: ITSGBody,
    ) -> TopmediaSongData:
        data: TopmediaResponse = await self._core.post(
            token=token,
            # Request **kwargs
            url_method=TopmediaMethod.MUSIC,
            endpoint=TopmediaEndpoint.SONG,
            data=TextMusicBody(
                **body.dict,
                token=token,
            ),
        )

        if data.status != 200:
            raise TopmediaError(data.status)

        return data.resp

    async def __fetch_text_speech_url(
        self,
        token: str,
        id: int,
    ) -> TopmediaResponse:
        data: TopmediaResponse = await self._core.get(
            token=token,
            # Request **kwargs
            url_method=TopmediaMethod.VOICE,
            endpoint=TopmediaEndpoint.DOWNLOAD.format(
                id=id,
            ),
            params=TopmediaTokenParams(
                token=token,
            ),
        )

        if data.status != 200:
            raise TopmediaError(data.status)

        return data

    async def __fetch_song_result(
        self,
        token: str,
        ids: list[int],
    ) -> TopmediaResponse:
        data: TopmediaResponse = await self._core.get(
            token=token,
            # Request **kwargs
            url_method=TopmediaMethod.MUSIC,
            endpoint=TopmediaEndpoint.RESULT,
            params=TopmediaMusicParams(
                ids=ids,
                token=token,
            ),
        )

        if data.status != 200:
            raise TopmediaError(data.status)

        return data

    def __create_speach_response(
        self,
        body: IT2SBody,
        speech_data: TopmediaSpeechData,
        oss_data: TopmediaResponse,
    ) -> TopmediaSpeechResponse:
        data = TopmediaSpeechResponse(
            speaker=body.speaker,
            name=speech_data.name,
            oss_url=oss_data.resp.url,
        )

        return TopmediaAPIResponseData(
            status=oss_data.status,
            message=oss_data.msg,
            data=data,
        )

    def __create_song_response(
        self,
        song_data: TopmediaResponse,
    ) -> TopmediaAPIResponseData:
        data: list[TopmediaSongResponse] = list(
            map(
                lambda song: TopmediaSongResponse(
                    title=song.title, song_url=song.song_id
                ),
                song_data.resp.result,
            )
        )
        return TopmediaAPIResponseData(
            status=song_data.status,
            message=song_data.msg,
            data=data,
        )

    async def text_to_speech(
        self,
        body: IT2SBody,
    ) -> TopmediaAPIResponse:
        account = await account_database.fetch_next_account()

        # account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> TopmediaResponse:
                    # await self.__fetch_token_status(
                    #     token=token,
                    # )

                    # await self.__fetch_slang_text_status(
                    #     token=token,
                    #     body=body,
                    # )

                    speech_data: TopmediaSpeechData = await self.__generate_text_speech(
                        token=token,
                        body=body,
                    )

                    oss_data: TopmediaResponse = await self.__fetch_text_speech_url(
                        token=token,
                        id=speech_data.id,
                    )

                    return TopmediaAPIResponse(
                        resp=self.__create_speach_response(
                            body,
                            speech_data,
                            oss_data,
                        ),
                    )

                data: TopmediaAPIResponse = await call(token)

                if data.resp.status == 200:
                    # return await self.__handle_success(
                    #     data,
                    #     account_id,
                    #     body,
                    # )
                    return data

                elif data.resp.status == 400:
                    raise TopmediaError(data.resp.status)

                last_err_code = data.resp.status

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.TOPMEDIA,
                    )

                    try:
                        data = await call(token)

                        if data.resp.status == 200:
                            # return await self.__handle_success(
                            #     data,
                            #     account_id,
                            #     body,
                            # )
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.resp.status)
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

    async def text_to_song(
        self,
        body: ITSGBody,
    ) -> TopmediaAPIResponse:
        account = await account_database.fetch_next_account()

        # account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> TopmediaAPIResponse:
                    generation_data: TopmediaSongData = await self.__generate_text_song(
                        token=token,
                        body=body,
                    )

                    music_data: TopmediaResponse = await self.__fetch_song_result(
                        token=token,
                        ids=generation_data.song_ids,
                    )

                    for attempt in range(max_attempts):
                        music_data: TopmediaResponse = await self.__fetch_song_result(
                            token=token,
                            ids=generation_data.song_ids,
                        )

                        is_ready: bool = isinstance(
                            music_data.resp, TopmediaMusicResponse
                        ) and all(
                            song.song_id is not None for song in music_data.resp.result
                        )

                        if is_ready:
                            return TopmediaAPIResponse(
                                message="Song",
                                resp=self.__create_song_response(music_data),
                            )

                        await sleep(10)

                data: TopmediaAPIResponse = await call(token)

                if data.resp.status == 200:
                    return data

                elif data.resp.status == 400:
                    raise TopmediaError(data.resp.status)

                last_err_code = data.resp.status

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.TOPMEDIA,
                    )

                    try:
                        data = await call(token)

                        if data.resp.status == 200:
                            return data
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.resp.status)
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
