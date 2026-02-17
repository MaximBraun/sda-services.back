# coding utf-8

from httpx import (
    HTTPError,
    Response,
)

from fastapi import HTTPException

from ..core import HttpClient

from ....domain.constants import XIMILAR_API_URLS

from ....domain.entities.ximilar import ITokenHeaders

from ....domain.typing.enums import RequestMethod

from ....interface.schemas.external import WanResponse


class XimilarCore(HttpClient):
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
            XIMILAR_API_URLS,  # Базовый URL из конфигурации
        )

    async def post(
        self,
        token: str = None,
        endpoint: str = "",
        *args,
        **kwargs,
    ):
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
            return await super().send_request(
                RequestMethod.POST,
                headers=ITokenHeaders(
                    token=token,
                ),
                endpoint=endpoint,
                *args,
                **kwargs,
            )
        except HTTPError as err:
            if err.response is not None:
                try:
                    return err.response.json()
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))

    async def get(
        self,
        token: str = None,
        endpoint: str = "",
        *args,
        **kwargs,
    ):
        """Отправка GET-запроса к PixVerse API.

        Args:
            *args: Позиционные аргументы для send_request:
                - endpoint (str): Конечная точка API
            **kwargs: Именованные аргументы для send_request

        Returns:
            dict[str, Any]: Ответ API в формате JSON

        """
        try:
            return await super().send_request(
                RequestMethod.POST,
                headers=ITokenHeaders(
                    token=token,
                ),
                endpoint=endpoint,
                *args,
                **kwargs,
            )
        except HTTPError as err:
            if err.response is not None:
                try:
                    return err.response.json()
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))
