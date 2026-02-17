# coding utf-8

from fastapi import Depends

from .....external.pixverse import (
    PixverseCore,
    PixVerseClient,
)

from ......interface.controllers.api.v1 import PixVerseController

from .....api.views.v1 import PixVerseView


class PixVerseClientFactory:
    @staticmethod
    def get() -> PixVerseClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return PixVerseClient(
            PixverseCore(),
        )


class PixVerseControllerFactory:
    @staticmethod
    def get(
        client: PixVerseClient = Depends(
            PixVerseClientFactory.get,
        ),
    ) -> PixVerseController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return PixVerseController(
            client,
        )


class PixVerseViewFactory:
    @staticmethod
    def create(
        controller: PixVerseController = Depends(
            PixVerseControllerFactory.get,
        ),
    ) -> PixVerseView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return PixVerseView(
            controller,
        )
