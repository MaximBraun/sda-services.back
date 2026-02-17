# coding utf-8

from fastapi import Depends

from .....external.wan import (
    WanCore,
    WanClient,
)

from ......interface.controllers.api.v1 import WanController

from .....api.views.v1 import WanView


class WanClientFactory:
    @staticmethod
    def get() -> WanClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return WanClient(
            core=WanCore(),
        )


class WanControllerFactory:
    @staticmethod
    def get(
        client: WanClient = Depends(
            WanClientFactory.get,
        ),
    ) -> WanController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return WanController(
            client,
        )


class WanViewFactory:
    @staticmethod
    def create(
        controller: WanController = Depends(
            WanControllerFactory.get,
        ),
    ) -> WanView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return WanView(
            controller,
        )
