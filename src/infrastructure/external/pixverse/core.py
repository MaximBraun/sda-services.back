# coding utf-8

from typing import Any

from httpx import HTTPError

from fastapi import HTTPException

from ..core import HttpClient

from ....domain.constants import PIXVERSE_API_URL

from ....domain.entities.pixverse import ITokenHeaders

from ....domain.typing.enums import RequestMethod

from ....interface.schemas.external import Response


class PixverseCore(HttpClient):
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
            PIXVERSE_API_URL,  # Базовый URL из конфигурации
        )

    async def post(
        self,
        token: str = None,
        *args,
        **kwargs,
    ) -> Response:
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
                    token=token,
                )
                if token
                else None,
                *args,
                **kwargs,
            )
            return Response(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return Response(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))

    async def get(
        self,
        token: str,
        *args,
        **kwargs,
    ) -> Response:
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
                    token=token,
                )
                if token
                else None,
                *args,
                **kwargs,
            )
            return Response(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return Response(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))
