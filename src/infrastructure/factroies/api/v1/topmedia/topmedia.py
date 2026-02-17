# coding utf-8

from fastapi import Depends

from .....external.topmedia import (
    TopmediaCore,
    TopmediaClient,
)

from ......interface.controllers.api.v1 import TopmediaController

from .....api.views.v1 import TopmediaView


class TopmediaClientFactory:
    @staticmethod
    def get() -> TopmediaClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return TopmediaClient(
            TopmediaCore(),
        )


class TopmediaControllerFactory:
    @staticmethod
    def get(
        client: TopmediaClient = Depends(
            TopmediaClientFactory.get,
        ),
    ) -> TopmediaController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return TopmediaController(
            client,
        )


class TopmediaViewFactory:
    @staticmethod
    def create(
        controller: TopmediaController = Depends(
            TopmediaControllerFactory.get,
        ),
    ) -> TopmediaView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return TopmediaView(
            controller,
        )
