# coding utf-8

from enum import StrEnum


class ConfEnv(StrEnum):
    """Перечисление возможных окружений приложения.

    Используется для определения текущего окружения (production, development, test)
    и соответствующей настройки поведения приложения.
    """

    PROD = "prod"
    """
    Production окружение (боевой режим работы).
    """

    DEV = "dev"
    """
    Development окружение (режим разработки).
    """

    TEST = "test"
    """
    Testing окружение (режим тестирования).
    """
