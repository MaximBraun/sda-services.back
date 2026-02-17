# coding utf-8

import os

from fastapi import UploadFile

from asyncio import sleep

from .core import CaloriesCore

from base64 import b64encode

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.entities.bot import IBotReporter

from ....domain.entities.chatgpt import CaloriesBody, CaloriesWeightBody

from ....interface.schemas.external import (
    ChatGPTCaloriesResponse,
    ChatGPTErrorResponse,
    ChatGPTCalories,
    ChatGPTError,
    ChatGPTWeightCalories,
    ChatGPTWeightCaloriesResponse,
)

from ....domain.constants import HEIF_EXTENSIONS

from ....domain.tools import convert_heic_to_jpg

from ....domain.errors import CaloriesError

from ....domain.typing.enums import ChatGPTEndpoint


conf: IConfEnv = app_conf()

telegram_bot = IBotReporter(
    conf,
)


class CaloriesClient:
    """Клиентский интерфейс для работы с ChatGPT API.

    Предоставляет удобные методы для основных операций с видео контентом:
    - Генерация видео из текста
    - Создание видео из изображений
    - Проверка статуса задач

    Args:
        core (ChatGPTCore): Базовый клиент для выполнения запросов
    """

    def __init__(
        self,
        core: CaloriesCore,
    ) -> None:
        self._core = core

    async def __handle_failure(
        self,
        last_error: ChatGPTError,
        status_code: int | None = None,
        extra: dict[str] = {},
    ) -> CaloriesError:
        error = CaloriesError(
            status_code=status_code if status_code is not None else 400,
            detail=last_error.message,
            extra=extra,
        )
        raise error

    async def photo_to_calories(
        self,
        image: UploadFile,
    ) -> ChatGPTCalories:
        max_attempts = 10

        last_error = None

        ext = str(os.path.splitext(image.filename)[-1]).lower()
        image_bytes = await image.read()

        if ext in HEIF_EXTENSIONS:
            image_bytes, ext, _ = await convert_heic_to_jpg(
                image_bytes,
            )

        image_base64 = b64encode(image_bytes).decode("utf-8")

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTCaloriesResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=CaloriesBody.create_image(
                            image_url=f"data:image/jpeg;base64,{image_base64}"
                        ),
                    )

                data: ChatGPTCaloriesResponse | ChatGPTErrorResponse = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def text_to_calories(
        self,
        description: str,
    ) -> ChatGPTCalories:
        max_attempts = 10

        last_error = None

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTCaloriesResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=CaloriesBody.create_text(
                            description=description,
                        ),
                    )

                data: ChatGPTCaloriesResponse | ChatGPTErrorResponse = await call(token)

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def text_to_weight_calories(
        self,
        description: str,
    ) -> ChatGPTWeightCalories:
        max_attempts = 10

        last_error = None

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTWeightCaloriesResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        weight=True,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=CaloriesWeightBody.create_text(
                            description=description,
                        ),
                    )

                data: ChatGPTWeightCaloriesResponse | ChatGPTErrorResponse = await call(
                    token
                )

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )

    async def photo_to_weight_calories(
        self,
        image: UploadFile,
    ) -> ChatGPTWeightCalories:
        max_attempts = 10

        last_error = None

        ext = str(os.path.splitext(image.filename)[-1]).lower()
        image_bytes = await image.read()

        if ext in HEIF_EXTENSIONS:
            image_bytes, ext, _ = await convert_heic_to_jpg(
                image_bytes,
            )

        image_base64 = b64encode(image_bytes).decode("utf-8")

        for attempt in range(max_attempts):
            token = conf.chatgpt_token
            try:

                async def call(
                    token: str,
                ) -> ChatGPTWeightCaloriesResponse | ChatGPTErrorResponse:
                    return await self._core.post(
                        token=token,
                        weight=True,
                        endpoint=ChatGPTEndpoint.CHAT,
                        body=CaloriesWeightBody.create_image(
                            image_url=f"data:image/jpeg;base64,{image_base64}"
                        ),
                    )

                data: ChatGPTWeightCaloriesResponse | ChatGPTErrorResponse = await call(
                    token
                )

                if not isinstance(data, ChatGPTErrorResponse):
                    return data.fetch_data()

                last_error = data.error

            except Exception:
                if attempt == max_attempts - 1:
                    try:
                        data = await call(token)

                        if not data.error:
                            print(data)
                            return data.fetch_data()

                    except Exception as final_err:
                        raise final_err
                    return await self.__handle_failure(last_error)
                await sleep(1)
        return await self.__handle_failure(
            last_error,
            extra={"Токен авторизации": token},
        )
