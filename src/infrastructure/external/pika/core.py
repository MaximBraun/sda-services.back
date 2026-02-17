# coding utf-8

from typing import Any

from httpx import HTTPError

from playwright.async_api import Page

from fastapi import HTTPException

from asyncio import sleep, create_task

from ..core import (
    HttpClient,
    WebSession,
)

from ....domain.constants import (
    TTL,
    PIKA_API_URLS,
    PIKA_SELECTORS,
    PIKA_AUTH_URL_PART,
)

from ....domain.errors import PikaError

from ....domain.typing.enums import PikaMethod

from ....domain.entities.pika import ITokenHeaders

from ....domain.typing.enums import RequestMethod

from ....interface.schemas.external import (
    PikaResponse,
    PikaAuthResponse,
    PikaAccountData,
    PikaCreditResponse,
    PikaGenerationResponse,
)


class PikaCore(HttpClient):
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
            PIKA_API_URLS,  # Базовый URL из конфигурации
        )

    async def post(
        self,
        token: str = None,
        api_key: str = None,
        cookie: str = None,
        is_serialized: bool = True,
        *args,
        **kwargs,
    ) -> bytes | PikaAuthResponse | PikaResponse:
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
                    api_key=api_key,
                    cookie=cookie,
                ),
                is_serialized=is_serialized,
                *args,
                **kwargs,
            )
            if is_serialized is False:
                return await response.aread()
            elif response.get("email"):
                return PikaAuthResponse(**response)
            elif response.get("success") is True:
                return PikaGenerationResponse.model_validate(
                    response,
                )
            return PikaResponse(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return PikaResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))

    async def get(
        self,
        token: str = None,
        api_key: str = None,
        cookie: str = None,
        *args,
        **kwargs,
    ) -> PikaAuthResponse | PikaResponse | PikaCreditResponse:
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
                    api_key=api_key,
                    cookie=cookie,
                ),
                *args,
                **kwargs,
            )
            if isinstance(response, list):
                return PikaCreditResponse(**response[0])
            if response.get("email"):
                return PikaAuthResponse(**response)
            return PikaResponse(**response)
        except HTTPError as err:
            if err.response is not None:
                try:
                    error_json = err.response.json()
                    return PikaResponse(**error_json)
                except Exception as json_err:
                    raise json_err
            raise HTTPException(status_code=502, detail=str(err))


class PikaSessionCore(WebSession):
    def __init__(
        self,
        headless: bool = True,
        wait_time: int = 3,
    ) -> None:
        super().__init__(
            headless=headless,
            wait_time=wait_time,
        )

        self._token: str | None = None
        self._api_key: str | None = None
        self._user_id: str | None = None
        self._cookies: str | None = None

    async def __capture_request(
        self,
        request,
    ) -> None:
        if PIKA_AUTH_URL_PART in request.url:
            auth: str | None = request.headers.get("authorization")
            api_key: str | None = request.headers.get("apikey")
            if auth:
                self._token = auth.removeprefix("Bearer ").strip()
                self._api_key = api_key

    async def __capture_response(
        self,
        response,
    ):
        if PIKA_AUTH_URL_PART in response.url:
            try:
                data = await response.json()
                self._user_id = data.get("id")
            except Exception as e:
                text = await response.text()
                print("DEBUG RESPONSE ERROR:", e, text[:300])

    async def fetch_auth_token(
        self,
        credentials: Any,
    ) -> PikaAccountData:
        async def auth_flow(
            page: Page,
        ) -> None:
            page.on(
                "request",
                self.__capture_request,
            )

            def handle_response(
                response,
            ) -> None:
                create_task(
                    self.__capture_response(response),
                )

            page.on(
                "response",
                handle_response,
            )

            await self.safe_open_page(
                page,
                PIKA_API_URLS.get(PikaMethod.AUTH),
            )

            await sleep(5)

            await self.wait_and_click(
                page,
                "button",
                has_text=PIKA_SELECTORS.get(PikaMethod.TEXT),
            )
            await self.wait_and_fill(
                page,
                PIKA_SELECTORS.get(PikaMethod.EMAIL),
                credentials.username,
            )
            await self.wait_and_fill(
                page,
                PIKA_SELECTORS.get(PikaMethod.PASSWORD),
                credentials.password,
            )
            await self.wait_and_click(
                page,
                PIKA_SELECTORS.get(PikaMethod.SUBMIT),
            )

            await sleep(20)

            cookies_list = await page.context.cookies()

            for _ in range(int(TTL.total_seconds() * 2)):
                if self._token and self._user_id:
                    break
                await sleep(1)

            filtered = [
                f"{c['name']}={c['value']}"
                for c in cookies_list
                if c["name"].startswith("sb-login-auth-token")
                or c["name"].startswith("ph_phc_")
            ]

            self._cookies = "; ".join(filtered) if len(filtered) >= 2 else None

        await self.with_browser(auth_flow)

        if (
            not self._token
            or not self._api_key
            or not self._user_id
            or not self._cookies
        ):
            raise PikaError(status_code=8)

        return PikaAccountData(
            token=self._token,
            api_key=self._api_key,
            user_id=self._user_id,
            cookies=self._cookies,
        )
