# coding utf-8

import os

from fastapi import UploadFile

from .core import PixverseCore

from uuid import uuid4

from asyncio import sleep

from math import ceil

from ....domain.conf import app_conf

from ....domain.errors import PixverseError

from ....domain.entities.core import (
    IConfEnv,
)

from ...orm.database.repositories import (
    PixverseAccountRepository,
    PixverseStyleRepository,
    PixverseTemplateRepository,
    UserGenerationRepository,
    UserDataRepository,
    PixverseAccountsTokensRepository,
)

from ....domain.repositories import IDatabase

from ....domain.entities.pixverse import (
    IT2VBody,
    II2VBody,
    IIT2VBody,
    IRVBody,
    LFBody,
    ITRVBody,
    IEVBody,
)

from ....domain.tools import (
    upload_file,
    update_account_token,
    convert_heic_to_jpg,
)

from ....domain.constants import HEIF_EXTENSIONS

from ....interface.schemas.external import (
    AuthRes,
    UserCredentials,
    Response,
    T2VBody,
    R2VBody,
    TE2VBody,
    I2VBody,
    IMGBody,
    VideoBody,
    StatusBody,
    UploadIMG,
    Resp,
    UTResp,
    GenerationStatus,
    TemplateBody,
    TokensResponse,
    EffectResponse,
    TemplateResp,
    GenerationData,
    UsrData,
)

from ....interface.schemas.api import Style, Template

from ....domain.typing.enums import PixverseEndpoint


conf: IConfEnv = app_conf()


account_database = PixverseAccountRepository(
    engine=IDatabase(conf),
)

style_database = PixverseStyleRepository(
    engine=IDatabase(conf),
)

templates_database = PixverseTemplateRepository(
    engine=IDatabase(conf),
)

user_generations_database = UserGenerationRepository(
    engine=IDatabase(conf),
)

user_data_database = UserDataRepository(
    engine=IDatabase(conf),
)

pixverse_account_token_database = PixverseAccountsTokensRepository(
    engine=IDatabase(conf),
)


class PixVerseClient:
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
        core: PixverseCore,
    ) -> None:
        self._core = core

    async def auth_user(
        self,
        account,
    ) -> AuthRes:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.AUTH,
            body=UserCredentials(
                username=account.username,
                password=account.password,
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )

            raise error
        return data.resp.result

    async def upload_token(
        self,
        token: str,
    ) -> UTResp:
        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.UPLOAD_TOKEN,
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            # await telegram_bot.send_error_message(error=error)

            raise error
        return data.resp

    async def upload_image(
        self,
        token: str,
        filename: str,
        size: int,
    ) -> bool:
        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.UPLOAD_IMAGE,
            body=IMGBody(
                images=[
                    UploadIMG(
                        name=filename,
                        size=size,
                        path=f"upload/{filename}",
                    ).dict
                ]
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            # await telegram_bot.send_error_message(error=error)

            raise error
        return True

    async def upload_video(
        self,
        token: str,
        filename: str,
        path: int,
    ) -> Response:
        data: Response = await self._core.post(
            token=token,
            endpoint=PixverseEndpoint.UPLOAD_VIDEO,
            body=VideoBody(
                name=filename,
                path=path,
            ),
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )
            # await telegram_bot.send_error_message(error=error)

            raise error
        return data

    async def __get_account_token(
        self,
        account,
    ) -> str:
        token = await pixverse_account_token_database.fetch_token(
            "account_id", account.id
        )
        if token is None:
            user: AuthRes = await self.auth_user(account)

            token = user.access_token

            await update_account_token(
                account,
                token,
            )

        return token

    async def __get_video_status(
        self,
        data: Response,
        id: int,
    ) -> GenerationStatus | None:
        for video in data.resp.data:
            if video.video_id == id:
                if video.video_status == 1 and video.first_frame:
                    return GenerationStatus(status="success", video_url=video.url)
                return GenerationStatus(
                    status="generating" if video.video_status == 10 else "error"
                )

    async def __reauthenticate(
        self,
        account,
    ) -> str:
        user: AuthRes = await self.auth_user(account)

        return user.access_token

    async def __handle_success(
        self,
        data: Response,
        account_id: int,
        body: I2VBody,
    ) -> Resp:
        await user_generations_database.add_record(
            GenerationData(
                generation_id=data.resp.video_id,
                account_id=account_id,
                user_id=body.user_id,
                app_id=body.app_id,
                app_name=os.getenv("APP_SERVICE", "pixverse").lower(),
            )
        )
        await user_data_database.create_or_update_user_data(
            UsrData(
                user_id=body.user_id,
                app_id=body.app_id,
            )
        )
        return data.resp

    async def __handle_failure(
        self,
        status_code: int,
        extra: dict[str] = {},
    ) -> PixverseError:
        error = PixverseError(
            status_code=10005 if status_code is None else status_code,
            extra=extra,
        )

        raise error

    async def generation_status(
        self,
        id: int,
    ) -> GenerationStatus:
        generation_data = await user_generations_database.fetch_generation(
            "generation_id",
            id,
        )

        if generation_data is None:
            raise PixverseError(status_code=500008)

        account = await account_database.fetch_account(
            "id",
            generation_data.account_id,
        )

        max_attempts = 10

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> Response:
                    return await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.STATUS,
                        body=StatusBody(),
                    )

                data: Response = await call(token)

                if data.err_code == 0:
                    return await self.__get_video_status(
                        data,
                        id,
                    )

                elif data.err_code == 10005:
                    raise PixverseError(data.err_code)

                last_err_code = data.err_code

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                    )

                    try:
                        data = await call(token)

                        if data.err_code == 0:
                            return await self.__get_video_status(
                                data,
                                id,
                            )

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.err_code)
                await sleep(1)

        return await self.__handle_failure(
            last_err_code,
            extra={
                "Данные аккаунта": {
                    "Имя аккаунта": account.username,
                    "Пароль аккаунта": account.password,
                }
            },
        )

    async def credits_amount(
        self,
        token: str,
    ) -> TokensResponse:
        data: Response = await self._core.get(
            token=token,
            endpoint=PixverseEndpoint.TOKEN,
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )

            raise error
        return data.resp

    async def fetch_styles(
        self,
        body: TemplateBody,
    ) -> list[TemplateResp]:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.RESTYLE_TEMPLATE,
            body=body,
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )

            raise error
        return data.resp.items

    async def fetch_templates(
        self,
    ) -> EffectResponse:
        data: Response = await self._core.post(
            endpoint=PixverseEndpoint.TEMPLATES,
        )
        if data.err_code != 0:
            error = PixverseError(
                status_code=data.err_code,
            )

            raise error
        return data.resp

    async def text_to_video(
        self,
        body: T2VBody,
    ) -> Resp:
        account = await account_database.fetch_next_account(
            body.app_id,
        )

        if account is None:
            raise PixverseError(status_code=955)

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(token: str) -> Response:
                    return await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.TEXT,
                        body=IT2VBody(
                            prompt=body.prompt,
                        ),
                    )

                data: Response = await call(token)

                if data.err_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        body,
                    )

                elif data.err_code == 10005:
                    raise PixverseError(data.err_code)

                last_err_code = data.err_code

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                    )

                    try:
                        data = await call(token)

                        if data.err_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                body,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.err_code)
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
        body: I2VBody,
        image: UploadFile,
    ) -> Resp:
        account = await account_database.fetch_next_account(
            body.app_id,
        )

        if account is None:
            raise PixverseError(status_code=955)

        account_id = account.id

        image_bytes: bytes = await image.read()

        ext = os.path.splitext(image.filename)[-1].lower().lstrip(".")

        if not ext:
            ext = "jpg"

        elif ext in HEIF_EXTENSIONS:
            image_bytes, ext, _ = await convert_heic_to_jpg(
                image_bytes,
            )

        filename = f"{uuid4()}.{ext}"

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> Response:
                    token_data: UTResp = await self.upload_token(token)

                    await upload_file(image_bytes, filename, **token_data.dict)

                    await self.upload_image(token, filename, size=len(image_bytes))

                    data = await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.IMAGE,
                        body=II2VBody(
                            img_path=filename,
                            img_url=filename,
                            prompt=body.prompt,
                        ),
                    )
                    return data

                data: Response = await call(token)

                if data.err_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        body,
                    )

                elif data.err_code == 10005:
                    raise PixverseError(data.err_code)

                last_err_code = data.err_code

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                    )

                    try:
                        data = await call(token)

                        if data.err_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                body,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.err_code)
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

    async def restyle_video(
        self,
        body: R2VBody,
        video: UploadFile,
    ):
        account = await account_database.fetch_next_account(
            body.app_id,
        )

        if account is None:
            raise PixverseError(status_code=955)

        account_id = account.id

        video_bytes: bytes = await video.read()

        ext = os.path.splitext(video.filename)[-1].lower().lstrip(".")

        if not ext:
            ext = "mp4"

        elif ext in HEIF_EXTENSIONS:
            video_bytes, ext, _ = await convert_heic_to_jpg(
                video_bytes,
            )

        filename = f"{uuid4()}.{ext}"

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> Response:
                    token_data: UTResp = await self.upload_token(
                        token,
                    )

                    style: Style | None = await style_database.fetch_style(
                        "template_id",
                        body.template_id,
                    )

                    if style is None:
                        raise PixverseError(status_code=500070)

                    await upload_file(
                        video_bytes,
                        filename,
                        **token_data.dict,
                    )

                    video_data: Response = await self.upload_video(
                        token,
                        filename,
                        filename,
                    )

                    video_path_for_frame = video_data.resp.path

                    frame_data = await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.LAST_FRAME,
                        body=LFBody(
                            video_path=video_path_for_frame,
                        ),
                    )

                    video_path = video_data.resp.path
                    video_url = video_data.resp.url
                    duration_video = ceil(video_data.resp.duration)

                    data: Response = await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.RESTYLE,
                        body=IRVBody(
                            video_path=video_path,
                            video_url=video_url,
                            video_duration=duration_video,
                            prompt=style.prompt,
                            last_frame_url=frame_data.resp.last_frame,
                        ),
                    )
                    return data

                data: Response = await call(token)

                if data.err_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        body,
                    )

                elif data.err_code == 10005:
                    raise PixverseError(data.err_code)

                last_err_code = data.err_code

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                    )

                    try:
                        data = await call(token)

                        if data.err_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                body,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.err_code)
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

    async def template_video(
        self,
        body: TE2VBody,
        image: UploadFile,
    ):
        account = await account_database.fetch_next_account(
            body.app_id,
        )

        if account is None:
            raise PixverseError(status_code=955)

        account_id = account.id

        image_bytes: bytes = await image.read()

        ext = os.path.splitext(image.filename)[-1].lower().lstrip(".")

        if not ext:
            ext = "jpg"

        elif ext in HEIF_EXTENSIONS:
            image_bytes, ext, _ = await convert_heic_to_jpg(
                image_bytes,
            )

        filename = f"{uuid4()}.{ext}"

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> Response:
                    token_data: UTResp = await self.upload_token(
                        token,
                    )

                    template: Template | None = await templates_database.fetch_template(
                        "template_id",
                        body.template_id,
                    )

                    if template is None:
                        raise PixverseError(status_code=500070)

                    await upload_file(
                        image_bytes,
                        filename,
                        **token_data.dict,
                    )

                    await self.upload_image(
                        token,
                        filename,
                        size=len(image_bytes),
                    )

                    data: Response = await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.IMAGE,
                        body=IIT2VBody(
                            img_path=filename,
                            img_url=filename,
                            prompt=template.prompt,
                            template_id=body.template_id,
                        ),
                    )
                    return data

                data: Response = await call(token)

                if data.err_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        body,
                    )

                elif data.err_code == 10005:
                    raise PixverseError(data.err_code)

                last_err_code = data.err_code

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                    )

                    try:
                        data = await call(token)

                        if data.err_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                body,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.err_code)
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

    async def extend_to_video(
        self,
        body: I2VBody,
        video: UploadFile,
    ) -> Resp:
        account = await account_database.fetch_next_account(
            body.app_id,
        )

        if account is None:
            raise PixverseError(status_code=955)

        account_id = account.id

        video_bytes: bytes = await video.read()

        ext = os.path.splitext(video.filename)[-1].lower().lstrip(".")

        if not ext:
            ext = "mp4"

        elif ext in HEIF_EXTENSIONS:
            video_bytes, ext, _ = await convert_heic_to_jpg(
                video_bytes,
            )

        filename = f"{uuid4()}.{ext}"

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> Response:
                    token_data: UTResp = await self.upload_token(
                        token,
                    )

                    await upload_file(
                        video_bytes,
                        filename,
                        **token_data.dict,
                    )

                    await self.upload_video(
                        token,
                        filename,
                        filename,
                    )

                    frame_data = await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.LAST_FRAME,
                        body=LFBody(
                            video_path=filename,
                        ),
                    )

                    data: Response = await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.EXTEND,
                        body=IEVBody(
                            video_path=filename,
                            video_url=filename,
                            video_duration=5,
                            prompt=body.prompt,
                            last_frame_url=frame_data.resp.last_frame,
                        ),
                    )
                    return data

                data: Response = await call(token)

                if data.err_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        body,
                    )

                elif data.err_code == 10005:
                    raise PixverseError(data.err_code)

                last_err_code = data.err_code

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                    )

                    try:
                        data = await call(token)

                        if data.err_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                body,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.err_code)
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

    async def transition_to_video(
        self,
        body: I2VBody,
        images: list[UploadFile],
    ) -> Resp:
        account = await account_database.fetch_next_account(
            body.app_id,
        )

        if account is None:
            raise PixverseError(status_code=955)

        account_id = account.id

        images_bytes: list[bytes] = [await image.read() for image in images]

        exts: list[str] = [
            os.path.splitext(image.filename)[1][1:].lower() or "jpg" for image in images
        ]

        for i, (image_bytes, ext) in enumerate(zip(images_bytes, exts)):
            if ext in HEIF_EXTENSIONS:
                image_bytes, ext, _ = await convert_heic_to_jpg(
                    image_bytes,
                )

                images_bytes[i] = image_bytes

                exts[i] = ext

        filenames = [f"{uuid4()}.{ext}" for ext in exts]

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> Response:
                    token_data: UTResp = await self.upload_token(token)

                    for image_bytes, filename in zip(images_bytes, filenames):
                        await upload_file(
                            image_bytes,
                            filename,
                            **token_data.dict,
                        )

                        await self.upload_image(
                            token,
                            filename,
                            size=len(image_bytes),
                        )

                    data = await self._core.post(
                        token=token,
                        endpoint=PixverseEndpoint.TRANSITION,
                        body=ITRVBody(
                            img_paths=filenames,
                            img_urls=filenames,
                            prompt=body.prompt,
                            prompts=[
                                body.prompt,
                            ],
                        ),
                    )
                    return data

                data: Response = await call(token)

                if data.err_code == 0:
                    return await self.__handle_success(
                        data,
                        account_id,
                        body,
                    )

                elif data.err_code == 10005:
                    raise PixverseError(data.err_code)

                last_err_code = data.err_code

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                    )

                    try:
                        data = await call(token)

                        if data.err_code == 0:
                            return await self.__handle_success(
                                data,
                                account_id,
                                body,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(data.err_code)
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
