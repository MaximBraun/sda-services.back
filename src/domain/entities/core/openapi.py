# coding utf-8

from typing import Annotated

from os import getenv

from pydantic import Field

from .base import ISchema


class IOpenAPI(ISchema):
    """Конфигурация OpenAPI/Swagger документации для API.

    Содержит параметры для настройки документации и интерактивной
    документации Swagger UI и ReDoc. Наследует функциональность
    сериализации от ISchema.

    Все URL-адреса указываются относительно корня API.
    """

    debug: Annotated[
        bool,
        Field(default=False),
    ]
    """Режим отладки для OpenAPI документации.
    
    Тип:
        bool
    Значение по умолчанию:
        False
    Влияние:
        - Включает/выключает дополнительные детали в документации
        - Может активировать дополнительные эндпоинты для разработки
    """

    docs_url: Annotated[
        str,
        Field(default="/docs"),
    ]
    """URL-адрес для доступа к Swagger UI интерфейсу.
    
    Тип:
        str
    Значение по умолчанию:
        "/docs"
    Особенности:
        - Если указана пустая строка, Swagger UI отключается
        - Относительный путь от корня API
    """

    openapi_prefix: Annotated[
        str,
        Field(default=f"/{getenv('APP_SERVICE', 'default')}"),
    ]
    """Префикс для всех OpenAPI-эндпоинтов.
    
    Тип:
        str
    Значение по умолчанию:
        "" (пустая строка - нет префикса)
    Использование:
        Полезно при развертывании за reverse-proxy
    """

    openapi_url: Annotated[
        str,
        Field(default="/openapi.json"),
    ]
    """URL-адрес для получения OpenAPI схемы в JSON формате.
    
    Тип:
        str
    Значение по умолчанию:
        "/openapi.json"
    Особенности:
        - Если указана пустая строка, генерация схемы отключается
        - Относительный путь от корня API
    """

    redoc_url: Annotated[
        str,
        Field(default="/redoc"),
    ]
    """URL-адрес для доступа к ReDoc интерфейсу.
    
    Тип:
        str
    Значение по умолчанию:
        "/redoc"
    Особенности:
        - Если указана пустая строка, ReDoc отключается
        - Альтернативный интерфейс документации
        - Относительный путь от корня API
    """

    version: Annotated[
        str,
        Field(default="0.1.0"),
    ]

    """Версия API, отображаемая в документации.
    
    Тип:
        str (семантическое версионирование)
    Значение по умолчанию:
        "0.1.0"
    Использование:
        - Отображается в Swagger UI и ReDoc
        - Используется в OpenAPI схеме
    """

    title: Annotated[
        str,
        Field(default=f"{getenv('APP_SERVICE', 'default').upper()} API SERVICE"),
    ]
