# coding utf-8

from typing import (
    AsyncGenerator,
    Any,
)

from datetime import (
    datetime,
    timezone,
)

from httpx import (
    AsyncClient,
    Response,
)

from asyncio import sleep

from playwright.async_api import (
    async_playwright,
    Browser,
    Page,
    TimeoutError,
)

from ...domain.entities.core import (
    ISchema,
)

from ...domain.constants import (
    TTL,
    DEFAULT_TIMEOUT,
)


class HttpClient:
    """Клиент для взаимодействия с Web3 API.

    Обеспечивает асинхронное подключение и выполнение запросов к Web3 сервисам.
    Поддерживает повторное использование соединений и автоматическое управление ресурсами.

    Args:
        url (str): Базовый URL API сервиса
        headers (dict[str, Any]): Заголовки для всех запросов (например, авторизация)
    """

    def __init__(
        self,
        url: str | dict[str, str],
    ) -> None:
        """Инициализация Web3 клиента.

        Args:
            url (str): Базовый URL (например, "https://api.web3.service")
            headers (dict): Стандартные заголовки для запросов
        """
        self._url = url

    async def get_client(
        self,
        headers: dict[str, Any],
        timeout: int,
    ) -> AsyncGenerator[AsyncClient, Any]:
        """Асинхронный генератор HTTP клиента с управлением контекстом.

        Yields:
            AsyncClient: Экземпляр асинхронного HTTP клиента

        """
        async with AsyncClient(headers=headers, timeout=timeout) as client:
            yield client

    async def __make_request(
        self,
        method: str,
        url_method: str | None,
        endpoint: str,
        headers: dict[str, Any],
        timeout: int,
        **kwargs: Any,
    ) -> AsyncGenerator[Response, Any]:
        """Внутренний метод выполнения запроса.

        Args:
            method (str): HTTP метод ("GET", "POST" и т.д.)
            endpoint (str): Конечная точка API
            **kwargs: Дополнительные параметры для запроса

        Yields:
            Response: Объект ответа от сервера

        """
        async for client in self.get_client(headers, timeout):
            api_url: str = (
                self._url.get(url_method) if url_method is not None else self._url
            )

            try:
                yield await client.request(
                    method,
                    url="".join((api_url, endpoint)),
                    **kwargs,
                )
            finally:
                await client.aclose()

    async def send_request(
        self,
        method: str,
        headers: ISchema,
        endpoint: str,
        url_method: str | None = None,
        timeout: int = 60,
        body: ISchema | list[ISchema] | None = None,
        files=None,
        params: ISchema | None = None,
        data: ISchema | None = None,
        is_serialized: bool = True,
    ) -> dict[str, Any]:
        """Основной метод отправки запроса к API.

        Args:
            method (str): HTTP метод ("GET", "POST" и т.д.)
            endpoint (str): Относительный путь конечной точки
            body (ISchema, optional): Тело запроса, соответствующее схеме

        Returns:
            dict[str, Any]: Ответ API в виде словаря

        """
        async for response in self.__make_request(
            method,
            url_method,
            endpoint,
            headers.dict if headers else None,
            timeout,
            json=[i.dict for i in body]
            if isinstance(body, list)
            else body.dict
            if body
            else None,
            files=files if files else None,
            params=params.dict if params else None,
            data=data.dict if data else None,
        ):
            if is_serialized:
                return response.json()
            return response


class WebSession:
    def __init__(
        self,
        headless: bool = True,
        wait_time: int = 10,
    ) -> None:
        self.headless = headless
        self.wait_time = wait_time
        self.cookies: dict[str, str] = {}
        self.user_agent: str = ""
        self.expires_at: datetime = datetime.min.replace(
            tzinfo=timezone.utc,
        )

    @property
    def is_expired(
        self,
    ) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at

    async def __launch_browser(
        self,
    ) -> Browser:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=self.headless,
        )
        return browser

    async def refresh(
        self,
        url: str,
    ) -> None:
        browser: Browser | None = None
        try:
            browser = await self.__launch_browser()
            page: Page = await browser.new_page()

            await page.goto(
                url,
                wait_until="domcontentloaded",
            )
            await sleep(self.wait_time)

            cookies_list = await page.context.cookies()
            self.cookies = {c["name"]: c["value"] for c in cookies_list}

            self.user_agent = await page.evaluate("() => navigator.userAgent")
            self.expires_at = datetime.now(timezone.utc) + TTL

        except TimeoutError as err:
            raise err
        finally:
            if browser:
                try:
                    await browser.close()
                except Exception as err:
                    raise err

    async def with_browser(
        self,
        func,
        *args,
        **kwargs,
    ) -> bool:
        browser: Browser | None = None
        try:
            browser = await self.__launch_browser()
            page: Page = await browser.new_page()

            return await func(
                page,
                *args,
                **kwargs,
            )
        finally:
            if browser:
                await browser.close()
            return True

    async def safe_open_page(
        self,
        page: Page,
        url: str,
        retries: int = 3,
    ) -> bool:
        for attempt in range(1, retries + 1):
            try:
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=DEFAULT_TIMEOUT,
                )
            except TimeoutError as err:
                if attempt == retries:
                    raise err
                await sleep(1)
            return True

    async def wait_and_click(
        self,
        page: Page,
        selector: str,
        *,
        has_text: str | None = None,
    ) -> bool:
        try:
            locator = (
                page.locator(
                    selector,
                    has_text=has_text,
                )
                if has_text
                else page.locator(selector)
            )

            await locator.wait_for(
                state="visible",
                timeout=DEFAULT_TIMEOUT,
            )
            await locator.click()
        except TimeoutError as err:
            raise err
        return True

    async def wait_and_fill(
        self,
        page: Page,
        selector: str,
        value: str,
    ) -> bool:
        try:
            await page.wait_for_selector(
                selector,
                state="visible",
                timeout=DEFAULT_TIMEOUT,
            )
            await page.fill(selector, value)
        except TimeoutError as err:
            raise err
        return True
