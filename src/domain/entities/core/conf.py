# coding utf-8

import logging

from typing import Annotated, Any

from os import getenv

from pydantic import Field

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from ...typing import TConf

from .openapi import IOpenAPI


class IConfEnv(BaseSettings):
    """Конфигурация среды приложения.

    Содержит настройки для работы приложения, включая:
    - Окружение приложения (production/staging/development)
    - Настройки API
    - Параметры логирования
    - Конфигурацию OpenAPI
    - Безопасность (разрешенные хосты, API-ключи)

    Настройки могут быть загружены из .env файла или переменных окружения.
    """

    app_env: Annotated[
        TConf,
        Field(default=getenv("APP_ENV")),
    ]
    """Окружение приложения (production/staging/development/etc).
    
    Тип:
        TConf: Перечисление возможных окружений
    Значение по умолчанию:
        Берется из переменной окружения APP_ENV
    """
    api_prefix: Annotated[
        str,
        Field(default="/api/v1"),
    ]
    """Префикс для всех API-эндпоинтов.
    
    Тип:
        str
    Значение по умолчанию:
        "/api/v1"
    """

    clickhouse_dsn_url: Annotated[
        str,
        Field(...),
    ]

    database_dsn_url: Annotated[
        str,
        Field(...),
    ]

    rabbitmq_dsn_url: Annotated[
        str,
        Field(...),
    ]
    redis_dsn_url: Annotated[
        str,
        Field(...),
    ]

    secret_key: Annotated[
        str,
        Field(...),
    ]

    algorithm: Annotated[
        str,
        Field(...),
    ]

    domain_url: Annotated[
        str,
        Field(...),
    ]

    chatgpt_token: Annotated[
        str,
        Field(...),
    ]

    rocket_token: Annotated[
        str,
        Field(...),
    ]

    telegram_bot_token: Annotated[
        str,
        Field(...),
    ]
    telegram_chat_id: Annotated[
        int,
        Field(...),
    ]

    allowed_hosts: Annotated[
        list[str],
        Field(default=["*"]),
    ]

    """Список разрешенных хостов (CORS).
    
    Тип:
        list[str]
    Значение по умолчанию:
        ["*"] (разрешены все хосты)
    """

    logging_level: Annotated[
        int,
        Field(default=logging.INFO),
    ]
    """Уровень логирования приложения.
    
    Тип:
        int (константы из модуля logging)
    Значение по умолчанию:
        logging.INFO
    """

    loggers: Annotated[
        tuple[str, ...],
        Field(default=("uvicorn.asgi", "uvicorn.access")),
    ]
    """Кортеж имен логгеров для настройки.
    
    Тип:
        tuple[str, ...]
    Значение по умолчанию:
        ("uvicorn.asgi", "uvicorn.access")
    """

    openapi_conf: Annotated[
        IOpenAPI,
        Field(default=IOpenAPI()),
    ]
    """Конфигурация OpenAPI/Swagger документации.
    
    Тип:
        IOpenAPI
    Значение по умолчанию:
        Дефолтный экземпляр IOpenAPI
    """

    @property
    def app_config(self) -> dict[str, Any]:
        """Возвращает конфигурацию приложения в виде словаря.

        Возвращает:
            dict[str, Any]: Словарь с конфигурацией,
            включая настройки OpenAPI
        """
        return self.openapi_conf.dict

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        validate_assignment=True,
        use_enum_values=True,
    )
    """Конфигурация модели Pydantic:
    
    - env_file: Загружать переменные из .env файла
    - extra: Разрешать дополнительные поля
    - validate_assignment: Проверять значения при присвоении
    - use_enum_values: Использовать значения Enum вместо объектов
    """
