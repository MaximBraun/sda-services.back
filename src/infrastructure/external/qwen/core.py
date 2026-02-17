# coding utf-8

from typing import Any

from httpx import HTTPError, Response

from fastapi import HTTPException

from ..core import HttpClient

from ....domain.constants import QWEN_API_URL

from ....domain.entities.qwen import ITokenHeaders

from ....domain.typing.enums import RequestMethod

from ....interface.schemas.external import (
    QwenAuthResponse,
    QwenResponse,
    QwenErrorResponse,
)


class QwenCore(HttpClient):
    """Базовый клиент для работы с TopMedia API.

    Наследует функциональность Web3 клиента и добавляет специализированные методы
    для взаимодействия с PixVerse API. Автоматически использует базовый URL сервиса.

    Args:
        headers (dict[str, Any]): Заголовки HTTP-запросов (должен содержать JWT)
    """

    def __init__(
        self,
    ) -> None:
        """Инициализация клиента PixVerse.

        Args:
            headers (dict): Заголовки запросов, обязательно включающие:
                - 'Token': Ключ авторизации
        """
        super().__init__(
            QWEN_API_URL,  # Базовый URL из конфигурации
        )

    async def post(
        self,
        token: str | None = None,
        is_serialized: bool = True,
        *args,
        **kwargs,
    ) -> dict[str, Any] | QwenAuthResponse | QwenResponse | QwenErrorResponse:
        """Отправка POST-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
                - body (ISchema, optional): Тело запроса
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        try:
            response: dict[str, Any] | Response = await super().send_request(
                RequestMethod.POST,
                headers=ITokenHeaders(
                    token=token if token else None,
                ),
                is_serialized=is_serialized,
                *args,
                **kwargs,
            )
            if not isinstance(response, Response):
                if response.get("data"):
                    return QwenResponse(**response)
                elif response.get("detail"):
                    return QwenErrorResponse(**response)
                return QwenAuthResponse(**response)

        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return QwenResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))

    async def get(
        self,
        token: str | None = None,
        *args,
        **kwargs,
    ) -> QwenResponse | QwenErrorResponse:
        """Отправка GET-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        try:
            response: dict[str, Any] = await super().send_request(
                RequestMethod.GET,
                headers=ITokenHeaders(
                    token=token if token else None,
                ),
                *args,
                **kwargs,
            )
            if response.get("detail"):
                return QwenErrorResponse(**response)
            return QwenResponse(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return QwenResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))
