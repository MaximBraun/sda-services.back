# coding utf-8

from typing import Any

from httpx import (
    HTTPError,
    Response,
)

from fastapi import HTTPException

from ..core import HttpClient

from ....domain.constants import WAN_API_URLS

from ....domain.entities.wan import ITokenHeaders

from ....domain.typing.enums import RequestMethod

from ....interface.schemas.external import WanResponse


class WanCore(HttpClient):
    """Базовый клиент для работы с PixVerse API.

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
            WAN_API_URLS,  # Базовый URL из конфигурации
        )

    async def post(
        self,
        cookie: str = None,
        is_serialized: bool = True,
        endpoint: str = "",
        *args,
        **kwargs,
    ) -> WanResponse | Response:
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
            response: dict[str, Any] = await super().send_request(
                RequestMethod.POST,
                headers=ITokenHeaders(
                    cookie=cookie,
                ),
                is_serialized=is_serialized,
                endpoint=endpoint,
                *args,
                **kwargs,
            )
            if is_serialized:
                return WanResponse(**response)
            return response
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return WanResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))

    async def get(
        self,
        cookie: str = None,
        *args,
        **kwargs,
    ) -> WanResponse:
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
                    cookie=cookie,
                ),
                *args,
                **kwargs,
            )
            return WanResponse(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return WanResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))
