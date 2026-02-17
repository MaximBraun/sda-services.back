# coding utf-8

from fastapi import Depends

from .....external.chatgpt import (
    ChatGPTCore,
    ChatGPTClient,
)

from ......interface.controllers.api.v1 import ChatGPTController

from .....api.views.v1 import ChatGPTView


class ChatGPTClientFactory:
    @staticmethod
    def get() -> ChatGPTClient:
        """
        Возвращает экземпляр PixVerseClient с инициализированным ядром.

        Returns:
            PixVerseClient: Клиент для взаимодействия с PixVerseCore.
        """
        return ChatGPTClient(
            ChatGPTCore(),
        )


class ChatGPTControllerFactory:
    @staticmethod
    def get(
        client: ChatGPTClient = Depends(
            ChatGPTClientFactory.get,
        ),
    ) -> ChatGPTController:
        """
        Возвращает контроллер PixVerseController, внедряя зависимость PixVerseClient.

        Args:
            client (PixVerseClient): Клиент PixVerse для работы с бизнес-логикой.

        Returns:
            PixVerseController: Контроллер для обработки запросов.
        """
        return ChatGPTController(
            client,
        )


class ChatGPTViewFactory:
    @staticmethod
    def create(
        controller: ChatGPTController = Depends(
            ChatGPTControllerFactory.get,
        ),
    ) -> ChatGPTView:
        """
        Создает представление PixVerseView с контроллером.

        Args:
            controller (PixVerseController): Контроллер бизнес-логики.

        Returns:
            PixVerseView: Представление для обработки API-запросов.
        """
        return ChatGPTView(
            controller,
        )
