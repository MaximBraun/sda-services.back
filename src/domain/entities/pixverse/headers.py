# coding utf-8

from typing import Annotated

from fake_useragent import UserAgent

from pydantic import Field

from uuid import uuid4

from ..core import ISchema


class IHeaders(ISchema):
    """Базовые HTTP-заголовки для запросов к AI API.

    Содержит обязательные и опциональные заголовки для взаимодействия
    с API искусственного интеллекта. Наследует функциональность
    сериализации от ISchema.

    Особенности:
    - Автоматическая генерация trace_id при отсутствии
    - Использование стандартных алиасов для заголовков
    """

    trace_id: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4()), alias="Ai-Trace-Id"),
    ]
    """Уникальный идентификатор цепочки запросов (trace ID).
    
    Тип:
        str (UUID в строковом формате)
    Значение по умолчанию:
        Автоматически генерируется при создании (uuid4)
    Алиас в заголовке:
        Ai-trace-id
    Назначение:
        Для сквозной трассировки запросов в распределенных системах
    """


class ITokenHeaders(IHeaders):
    token: Annotated[
        str | None,
        Field(default=None, alias="Token"),
    ]
    """ Ключ аутентификации (JWT) для API.
    
    Тип:
        str
    Обязательное поле:
        Да
    Алиас в заголовке:
        Token
    """

    accept: Annotated[
        str,
        Field(
            default="application/json, text/plain, */*",
        ),
    ]

    # user_agent: Annotated[
    #     str,
    #     Field(default=UserAgent().random, alias="User-Agent"),
    # ]

    platform: Annotated[
        str,
        Field(default="Web", alias="x-platform"),
    ]

    content_type: Annotated[
        str,
        Field(default="application/json", alias="content-type"),
    ]

    # connection: Annotated[
    #     str,
    #     Field(default="close", alias="Connection"),
    # ]
