# coding utf-8

from fastapi import Depends

from .....external.cosmetic import (
    CosmeticCore,
    CosmeticClient,
)

from ......interface.controllers.api.v1 import CosmeticController

from .....api.views.v1 import CosmeticView


class CosmeticClientFactory:
    @staticmethod
    def get() -> CosmeticClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return CosmeticClient(
            CosmeticCore(),
        )


class CosmeticControllerFactory:
    @staticmethod
    def get(
        client: CosmeticClient = Depends(
            CosmeticClientFactory.get,
        ),
    ) -> CosmeticController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return CosmeticController(
            client,
        )


class CosmeticViewFactory:
    @staticmethod
    def create(
        controller: CosmeticController = Depends(
            CosmeticControllerFactory.get,
        ),
    ) -> CosmeticView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return CosmeticView(
            controller,
        )
