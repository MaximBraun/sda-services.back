# coding utf-8

from fastapi import Depends

from .....external.pika import (
    PikaCore,
    PikaSessionCore,
    PikaClient,
)

from ......interface.controllers.api.v1 import PikaController

from .....api.views.v1 import PikaView


class PikaClientFactory:
    @staticmethod
    def get() -> PikaClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return PikaClient(
            core=PikaCore(),
            session=PikaSessionCore(),
        )


class PikaControllerFactory:
    @staticmethod
    def get(
        client: PikaClient = Depends(
            PikaClientFactory.get,
        ),
    ) -> PikaController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return PikaController(
            client,
        )


class PikaViewFactory:
    @staticmethod
    def create(
        controller: PikaController = Depends(
            PikaControllerFactory.get,
        ),
    ) -> PikaView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return PikaView(
            controller,
        )
