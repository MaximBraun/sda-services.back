# coding utf-8

from .core import QwenCore

from os import getenv

from fastapi import (
    HTTPException,
    UploadFile,
)

from uuid import uuid4

from asyncio import sleep

from json import loads

from ddgs import DDGS

from ....domain.conf import app_conf

from ....domain.errors import QwenError

from ....domain.typing.enums import (
    QwenEndpoint,
    AccountProjectToken,
)

from ....domain.entities.core import (
    IConfEnv,
)

from ....domain.entities.qwen import (
    IT2IBody,
    IT2TBody,
    II2RBody,
    IP2BBody,
    IT2CBody,
    IT2PBody,
    QwenLoginBody,
    IQwenChat,
    IQwenPhotoBody,
    IQwenChatMessage,
    IPhotoBody,
    IQwenFile,
    IQwenFileInfo,
)

from ....domain.entities.chatgpt import R2PBodyPrompt

from ...orm.database.models import (
    QwenAccounts,
    QwenAccountsTokens,
)

from ...orm.database.repositories import (
    QwenAccountTokenRepository,
    QwenAccountRepository,
    PhotoGeneratorTemplateRepository,
    UserGenerationRepository,
    UserDataRepository,
)

from ....domain.repositories import IDatabase

from ....domain.tools import (
    update_account_token,
    upload_qwen_file,
)

from ....interface.schemas.external import (
    QwenResponse,
    QwenAuthResponse,
    QwenErrorResponse,
    QwenMessageContent,
    QwenPhotoAPIResponse,
    QwenUploadData,
    ChatGPTCalories,
    ChatGPTInstagram,
    ChatGPTCosmetic,
    ChatGPTGemstone,
    GenerationData,
    UsrData,
    SharkDectorFactMessage,
    DialogImageAnalysisMessage,
)


conf: IConfEnv = app_conf()


account_database = QwenAccountRepository(
    engine=IDatabase(conf),
)


account_token_database = QwenAccountTokenRepository(
    engine=IDatabase(conf),
)


template_database = PhotoGeneratorTemplateRepository(
    engine=IDatabase(conf),
)


user_generations_database = UserGenerationRepository(
    engine=IDatabase(conf),
)


user_data_database = UserDataRepository(
    engine=IDatabase(conf),
)


class QwenClient:
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
        core: QwenCore,
    ) -> None:
        self._core = core

    async def auth_user_account(
        self,
        account: QwenAccounts,
    ) -> str:
        data: QwenAuthResponse | QwenErrorResponse = await self._core.post(
            # Request **kwargs
            endpoint=QwenEndpoint.AUTH,
            body=QwenLoginBody(
                email=account.username,
                password=account.password,
            ),
        )

        if not isinstance(data, QwenAuthResponse):
            error = QwenError(
                status_code=409,
            )

            raise error
        return data.token

    async def __fetch_account_user_id(
        self,
        account_id: int,
    ) -> str:
        account = await account_database.fetch_with_filters(
            id=account_id,
        )
        return account.user_id

    def __get_media_content(
        self,
        data: QwenResponse,
    ) -> str:
        last_generation_id: str = data.resp.current_id

        if last_generation_id is not None:
            content_list: list[QwenMessageContent] = data.resp.chat.history.messages[
                last_generation_id
            ].content_list

            return content_list[0].content

    async def __handle_failure(
        self,
        status_code: int,
        detail: str,
        extra: dict[str] = {},
    ) -> QwenError:
        error = QwenError(
            status_code=status_code if status_code is not None else 400,
            detail=detail,
            extra=extra,
        )

        raise error

    async def __handle_success(
        self,
        app_id: str,
        user_id: str,
        data: QwenPhotoAPIResponse | ChatGPTInstagram,
    ) -> QwenPhotoAPIResponse:
        await user_generations_database.add_record(
            GenerationData(
                user_id=user_id,
                app_id=app_id,
                app_name=getenv("APP_SERVICE", "qwen").lower(),
                generation_url=data.media_url
                if isinstance(data, QwenPhotoAPIResponse)
                else "",
            )
        )
        await user_data_database.create_or_update_user_data(
            UsrData(
                user_id=user_id,
                app_id=app_id,
            )
        )
        return data

    async def __fetch_upload_token(
        self,
        token: str,
        image: UploadFile,
    ) -> QwenUploadData:
        data: QwenResponse = await self._core.post(
            token=token,
            # **kwargs
            endpoint=QwenEndpoint.MEDIA_TOKEN,
            body=IPhotoBody(
                filesize=image.size,
            ),
        )

        return data.resp

    async def __get_account_token(
        self,
        account: QwenAccounts,
    ) -> str:
        token_data: QwenAccountsTokens = (
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
                project=AccountProjectToken.QWEN,
            )

        return token

    async def __reauthenticate(
        self,
        account: QwenAccounts,
    ) -> str:
        return await self.auth_user_account(
            account,
        )

    async def __generate_new_chat(
        self,
        token: str,
        chat_type: str,
    ) -> str:
        data: QwenResponse | QwenErrorResponse = await self._core.post(
            token=token,
            # Request **kwargs
            endpoint=QwenEndpoint.CHAT,
            body=IQwenChat(
                chat_type=chat_type,
            ),
        )

        if not isinstance(data, QwenResponse):
            raise HTTPException(
                status_code=400,
                detail=data.detail,
            )

        return data.resp.id

    async def __generate_file_data(
        self,
        image: UploadFile,
        uploaded_image: QwenUploadData,
        user_id: str,
    ) -> IQwenFile:
        file_size = image.file.tell()

        return IQwenFile(
            id=uploaded_image.file_id,
            url=uploaded_image.file_url,
            size=file_size,
            name=image.filename,
            file_type=image.content_type,
            file=IQwenFileInfo(
                filename=image.filename,
                id=uploaded_image.file_id,
                meta={
                    "content_type": image.content_type,
                    "name": image.filename,
                    "size": file_size,
                },
                user_id=user_id,
            ),
        )

    async def __generate_photo(
        self,
        token: str,
        chat_id: str,
        body: IT2IBody,
        chat_type: str,
        user_id: str | None = None,
        image: UploadFile | None = None,
        uploaded_image: QwenUploadData | None = None,
    ) -> str:
        child_id: str = str(uuid4())

        if image and uploaded_image is not None:
            file = await self.__generate_file_data(
                image,
                uploaded_image,
                user_id,
            )

        message = IQwenChatMessage(
            content=body.prompt,
            children_ids=[child_id],
            chat_type=chat_type,
            files=[
                file,
            ]
            if image and uploaded_image is not None
            else [],
        )

        request_body: IQwenPhotoBody = IQwenPhotoBody(
            chat_id=chat_id,
            stream=True,
            messages=[
                message,
            ],
        )

        await self._core.post(
            token=token,
            is_serialized=False,
            # Request **kwargs
            endpoint=QwenEndpoint.GENERATE.format(
                chat_id=chat_id,
            ),
            body=request_body,
        )

        return child_id

    async def __fetch_media_content(
        self,
        token: str,
        chat_id: str,
    ) -> str:
        data: QwenResponse | QwenErrorResponse = await self._core.get(
            token=token,
            # Request **kwargs
            endpoint=QwenEndpoint.RESULT.format(
                chat_id=chat_id,
            ),
        )

        if not isinstance(data, QwenResponse):
            raise HTTPException(
                status_code=400,
                detail=data.detail,
            )

        return self.__get_media_content(data)

    def __find_images(
        self,
        name: str,
        max_results: int = 5,
        retries: int = 10,
    ):
        for _ in range(retries):
            with DDGS() as ddgs:
                images = [
                    r.get("image")
                    for r in ddgs.images(f"{name} gemstone", max_results=max_results)
                ]
            if not images:
                continue
            return images
        return []

    async def text_to_photo(
        self,
        body: IT2IBody,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        account = await account_database.fetch_next_account()

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="t2i",
                    )

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=body,
                        chat_type="t2i",
                    )

                    media = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return QwenPhotoAPIResponse(
                        media_url=media,
                    )

                data: QwenPhotoAPIResponse = await call(token)

                if isinstance(data, QwenPhotoAPIResponse):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, QwenPhotoAPIResponse):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def photo_to_photo(
        self,
        body: IT2IBody,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        account = await account_database.fetch_next_account()

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        image_bytes: bytes = await image.read()

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    uploaded_image: QwenUploadData = await self.__fetch_upload_token(
                        token=token,
                        image=image,
                    )

                    await upload_qwen_file(
                        uploaded_image,
                        image_bytes=image_bytes,
                    )

                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="image_edit",
                    )

                    user_id: str = await self.__fetch_account_user_id(
                        account_id=account_id,
                    )

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=body,
                        chat_type="image_edit",
                        image=image,
                        uploaded_image=uploaded_image,
                        user_id=user_id,
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return QwenPhotoAPIResponse(
                        media_url=media,
                    )

                data: QwenPhotoAPIResponse = await call(token)

                if isinstance(data, QwenPhotoAPIResponse):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, QwenPhotoAPIResponse):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def template_to_photo(
        self,
        body: IT2TBody,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        account = await account_database.fetch_next_account()

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        image_bytes: bytes = await image.read()

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    uploaded_image: QwenUploadData = await self.__fetch_upload_token(
                        token=token,
                        image=image,
                    )

                    await upload_qwen_file(
                        uploaded_image,
                        image_bytes=image_bytes,
                    )

                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="image_edit",
                    )

                    user_id: str = await self.__fetch_account_user_id(
                        account_id=account_id,
                    )

                    template = await template_database.fetch_with_filters(
                        id=body.template_id
                    )

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=template,
                        chat_type="image_edit",
                        image=image,
                        uploaded_image=uploaded_image,
                        user_id=user_id,
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return QwenPhotoAPIResponse(
                        media_url=media,
                    )

                data: QwenPhotoAPIResponse = await call(token)

                if isinstance(data, QwenPhotoAPIResponse):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, QwenPhotoAPIResponse):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def photo_to_toybox(
        self,
        body: IP2BBody,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        account = await account_database.fetch_next_account()

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        image_bytes: bytes = await image.read()

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    uploaded_image: QwenUploadData = await self.__fetch_upload_token(
                        token=token,
                        image=image,
                    )

                    await upload_qwen_file(
                        uploaded_image,
                        image_bytes=image_bytes,
                    )

                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="image_edit",
                    )

                    user_id: str = await self.__fetch_account_user_id(
                        account_id=account_id,
                    )

                    if not body.box_color or body.box_name or body.in_box:
                        prompted_body = await template_database.fetch_with_filters(
                            id=body.template_id
                        )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.toybox(
                        box_color=body.box_color,
                        in_box=body.in_box,
                        box_name=body.box_name,
                    )

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="image_edit",
                        image=image,
                        uploaded_image=uploaded_image,
                        user_id=user_id,
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return QwenPhotoAPIResponse(
                        media_url=media,
                    )

                data: QwenPhotoAPIResponse = await call(token)

                if isinstance(data, QwenPhotoAPIResponse):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, QwenPhotoAPIResponse):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def reshape_to_photo(
        self,
        body: II2RBody,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> QwenPhotoAPIResponse:
        account = await account_database.fetch_next_account()

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        image_bytes: bytes = await image.read()

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    uploaded_image: QwenUploadData = await self.__fetch_upload_token(
                        token=token,
                        image=image,
                    )

                    await upload_qwen_file(
                        uploaded_image,
                        image_bytes=image_bytes,
                    )

                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="image_edit",
                    )

                    user_id: str = await self.__fetch_account_user_id(
                        account_id=account_id,
                    )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.reshape(
                        body.area,
                        body.strength,
                    )

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="image_edit",
                        user_id=user_id,
                        image=image,
                        uploaded_image=uploaded_image,
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return QwenPhotoAPIResponse(
                        media_url=media,
                    )

                data: QwenPhotoAPIResponse = await call(token)

                if isinstance(data, QwenPhotoAPIResponse):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, QwenPhotoAPIResponse):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def photo_to_cosmetic(
        self,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> list[ChatGPTCosmetic]:
        account = await account_database.fetch_next_account()

        account_id = account.id

        max_attempts = 10

        last_err_code = None

        image_bytes: bytes = await image.read()

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    uploaded_image: QwenUploadData = await self.__fetch_upload_token(
                        token=token,
                        image=image,
                    )

                    await upload_qwen_file(
                        uploaded_image,
                        image_bytes=image_bytes,
                    )

                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="t2t",
                    )

                    user_id: str = await self.__fetch_account_user_id(
                        account_id=account_id,
                    )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.cosmetic()

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="t2t",
                        user_id=user_id,
                        image=image,
                        uploaded_image=uploaded_image,
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return list(
                        ChatGPTCosmetic.model_validate(
                            item,
                        )
                        for item in loads(media)
                    )

                data: list[ChatGPTCosmetic] = await call(token)

                if isinstance(data, list[ChatGPTCosmetic]):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, list[ChatGPTCosmetic]):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def text_to_calories(
        self,
        body: IT2CBody,
        app_id: str,
        user_id: str,
    ) -> ChatGPTCalories:
        account = await account_database.fetch_next_account()

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="t2t",
                    )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.calories(
                        description=body.description,
                    )

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="t2t",
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return ChatGPTCalories(
                        **loads(media),
                    )

                data: ChatGPTCalories = await call(token)

                if isinstance(data, ChatGPTCalories):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, ChatGPTCalories):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def photo_to_calories(
        self,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> ChatGPTCalories:
        account = await account_database.fetch_next_account()

        account_id = account.id

        max_attempts = 1

        last_err_code = None

        image_bytes: bytes = await image.read()

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    uploaded_image: QwenUploadData = await self.__fetch_upload_token(
                        token=token,
                        image=image,
                    )

                    await upload_qwen_file(
                        uploaded_image,
                        image_bytes=image_bytes,
                    )

                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="t2t",
                    )

                    user_id: str = await self.__fetch_account_user_id(
                        account_id=account_id,
                    )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.calories()

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="t2t",
                        user_id=user_id,
                        image=image,
                        uploaded_image=uploaded_image,
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return ChatGPTCalories(
                        **loads(media),
                    )

                data: QwenPhotoAPIResponse = await call(token)

                if isinstance(data, ChatGPTCalories):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, ChatGPTCalories):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def text_to_post(
        self,
        body: IT2PBody,
        app_id: str,
        user_id: str,
    ) -> ChatGPTInstagram:
        account = await account_database.fetch_next_account()

        max_attempts = 1

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> ChatGPTInstagram:
                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="t2t",
                    )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.instagram(
                        body.prompt,
                    )

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="t2t",
                    )

                    media = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return ChatGPTInstagram(
                        **loads(media),
                    )

                data: ChatGPTInstagram = await call(token)

                if len(data.description) == 0:
                    raise QwenError(
                        status_code=400,
                        detail="The described text is too small, add a few more words",
                    )

                elif isinstance(data, ChatGPTInstagram):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if len(data.description) == 0:
                            raise QwenError(
                                status_code=400,
                                detail="The described text is too small, add a few more words",
                            )

                        elif isinstance(data, ChatGPTInstagram):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def photo_to_gamestone(
        self,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> ChatGPTGemstone:
        account = await account_database.fetch_next_account()

        account_id = account.id

        max_attempts = 1

        last_err_code = None

        image_bytes: bytes = await image.read()

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    uploaded_image: QwenUploadData = await self.__fetch_upload_token(
                        token=token,
                        image=image,
                    )

                    await upload_qwen_file(
                        uploaded_image,
                        image_bytes=image_bytes,
                    )

                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="t2t",
                    )

                    user_id: str = await self.__fetch_account_user_id(
                        account_id=account_id,
                    )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.gamestone()

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="t2t",
                        user_id=user_id,
                        image=image,
                        uploaded_image=uploaded_image,
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    loaded_media = loads(media)

                    images = self.__find_images(
                        loaded_media.get("name"),
                    )

                    if len(loaded_media) <= 0:
                        raise QwenError(
                            status_code=404,
                            detail="Gemstone could not be identified",
                        )
                    return ChatGPTGemstone(
                        **loaded_media,
                        images=images,
                    )

                data: ChatGPTGemstone = await call(token)

                if isinstance(data, ChatGPTGemstone):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except QwenError as err:
                raise err

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, ChatGPTGemstone):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def fetch_day_fact(
        self,
        app_id: str,
        user_id: str,
    ) -> SharkDectorFactMessage:
        account = await account_database.fetch_next_account()

        max_attempts = 10

        last_err_code = None

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> SharkDectorFactMessage:
                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="t2t",
                    )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.day_fact()

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="t2t",
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return SharkDectorFactMessage(
                        **loads(media),
                    )

                data: SharkDectorFactMessage = await call(token)

                if isinstance(data, SharkDectorFactMessage):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, SharkDectorFactMessage):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )

    async def photo_to_honesty(
        self,
        image: UploadFile,
        app_id: str,
        user_id: str,
    ) -> DialogImageAnalysisMessage:
        account = await account_database.fetch_next_account()

        account_id = account.id

        max_attempts = 1

        last_err_code = None

        image_bytes: bytes = await image.read()

        for attempt in range(max_attempts):
            token = await self.__get_account_token(
                account,
            )

            try:

                async def call(
                    token: str,
                ) -> QwenPhotoAPIResponse:
                    uploaded_image: QwenUploadData = await self.__fetch_upload_token(
                        token=token,
                        image=image,
                    )

                    await upload_qwen_file(
                        uploaded_image,
                        image_bytes=image_bytes,
                    )

                    chat_id: str = await self.__generate_new_chat(
                        token=token,
                        chat_type="t2t",
                    )

                    user_id: str = await self.__fetch_account_user_id(
                        account_id=account_id,
                    )

                    prompted_body: R2PBodyPrompt = R2PBodyPrompt.honestly()

                    await self.__generate_photo(
                        token=token,
                        chat_id=chat_id,
                        body=prompted_body,
                        chat_type="t2t",
                        user_id=user_id,
                        image=image,
                        uploaded_image=uploaded_image,
                    )

                    media: str = await self.__fetch_media_content(
                        token=token,
                        chat_id=chat_id,
                    )

                    return DialogImageAnalysisMessage.model_validate(
                        loads(media),
                    )

                data: DialogImageAnalysisMessage = await call(token)

                if isinstance(data, DialogImageAnalysisMessage):
                    return await self.__handle_success(
                        app_id,
                        user_id,
                        data,
                    )

            except QwenError as err:
                raise err

            except Exception:
                if attempt == max_attempts - 1:
                    token = await self.__reauthenticate(account)

                    await update_account_token(
                        account,
                        token,
                        project=AccountProjectToken.QWEN,
                    )

                    try:
                        data = await call(token)

                        if isinstance(data, DialogImageAnalysisMessage):
                            return await self.__handle_success(
                                app_id,
                                user_id,
                                data,
                            )
                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(
                        400,
                        detail=last_err_code,
                    )
                await sleep(1)

        return await self.__handle_failure(
            400,
            detail=last_err_code,
            extra={
                "Данные аккаунта": {
                    "логин": account.username,
                    "пароль": account.password,
                }
            },
        )
