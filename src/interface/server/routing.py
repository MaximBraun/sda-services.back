# coding utf-8

from typing import (
    List,
    Any,
    Generator,
)

from fastapi import FastAPI, APIRouter

from ...domain.entities.core import IConfEnv


class AppRouting:
    """Менеджер регистрации роутеров в FastAPI приложении.

    Обеспечивает централизованную регистрацию API роутеров
    с автоматической обработкой префиксов из конфигурации.

    Args:
        app (FastAPI): Экземпляр FastAPI приложения
        config (IConfEnv): Конфигурация приложения
        routers (List[APIRouter]): Список роутеров для регистрации
    """

    def __init__(
        self,
        app: FastAPI,
        config: IConfEnv,
        routers: List[APIRouter],
    ) -> None:
        """Инициализация менеджера роутинга.

        Args:
            app: Экземпляр FastAPI приложения
            config: Конфигурация с настройками API (префикс и др.)
            routers: Список роутеров для регистрации
        """
        self._config = config
        self._app = app
        self._routers = routers

    def create(
        self,
    ) -> List[APIRouter]:
        """Регистрирует все роутеры в приложении.

        Returns:
            List[APIRouter]: Список зарегистрированных роутеров

        """
        routers: map[APIRouter] = map(
            lambda router: next(
                self.__register_router(router),
            ),
            self._routers,
        )
        return list(routers)

    def __register_router(
        self,
        router: APIRouter,
    ) -> Generator[APIRouter, Any, None]:
        """Внутренний метод регистрации одного роутера.

        Args:
            router: Роутер для регистрации

        Yields:
            APIRouter: Зарегистрированный роутер

        """
        yield self._app.include_router(
            router,
            prefix=self._config.api_prefix,
        )
