# coding utf-8

from enum import StrEnum, IntEnum

from fastapi import status


class RequestMethod(StrEnum):
    GET = "GET"
    """
    Метод GET - получение ресурса.
    """

    POST = "POST"
    """
    Метод POST - создание ресурса.
    """


class RequestError(IntEnum):
    FORBIDDEN = status.HTTP_401_UNAUTHORIZED
