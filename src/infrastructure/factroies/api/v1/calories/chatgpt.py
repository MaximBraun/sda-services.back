# coding utf-8

from fastapi import Depends

from .....external.calories import (
    CaloriesCore,
    CaloriesClient,
)

from ......interface.controllers.api.v1 import CaloriesController

from .....api.views.v1 import CaloriesView


class CaloriesClientFactory:
    @staticmethod
    def get() -> CaloriesClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return CaloriesClient(
            CaloriesCore(),
        )


class CaloriesControllerFactory:
    @staticmethod
    def get(
        client: CaloriesClient = Depends(
            CaloriesClientFactory.get,
        ),
    ) -> CaloriesController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return CaloriesController(
            client,
        )


class CaloriesViewFactory:
    @staticmethod
    def create(
        controller: CaloriesController = Depends(
            CaloriesControllerFactory.get,
        ),
    ) -> CaloriesView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return CaloriesView(
            controller,
        )
