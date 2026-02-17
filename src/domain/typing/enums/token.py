# coding utf-8

from enum import StrEnum, IntEnum


class TokenType(StrEnum):
    access: str = "access"
    refresh: str = "refresh"


class TokenTitle(StrEnum):
    access: str = "access_token"
    refresh: str = "refresh_token"


class TokenExpiry(IntEnum):
    access: int = 3600
    refresh: int = 86400


class AccountProjectToken(StrEnum):
    PIXVERSE = "pixverse"

    TOPMEDIA = "topmedia"

    QWEN = "qwen"
