# coding utf-8

from fastapi import Depends

from .....external.ximilar import (
    XimilarCore,
    XimilarClient,
)

from ......interface.controllers.api.v1 import XimilarController

from .....api.views.v1 import XimilarView


class XimilarClientFactory:
    @staticmethod
    def get() -> XimilarClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return XimilarClient(
            core=XimilarCore(),
        )


class XimilarControllerFactory:
    @staticmethod
    def get(
        client: XimilarClient = Depends(
            XimilarClientFactory.get,
        ),
    ) -> XimilarController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return XimilarController(
            client,
        )


class XimilarViewFactory:
    @staticmethod
    def create(
        controller: XimilarController = Depends(
            XimilarControllerFactory.get,
        ),
    ) -> XimilarView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return XimilarView(
            controller,
        )
