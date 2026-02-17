# coding utf-8

from fastapi import Depends

from .....external.qwen import (
    QwenCore,
    QwenClient,
)

from ......interface.controllers.api.v1 import QwenController

from .....api.views.v1 import QwenView


class QwenClientFactory:
    @staticmethod
    def get() -> QwenClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return QwenClient(
            QwenCore(),
        )


class QwenControllerFactory:
    @staticmethod
    def get(
        client: QwenClient = Depends(
            QwenClientFactory.get,
        ),
    ) -> QwenController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return QwenController(
            client,
        )


class QwenViewFactory:
    @staticmethod
    def create(
        controller: QwenController = Depends(
            QwenControllerFactory.get,
        ),
    ) -> QwenView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return QwenView(
            controller,
        )
