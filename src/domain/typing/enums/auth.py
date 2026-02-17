# coding utf-8

from enum import StrEnum


class AuthType(StrEnum):
    bearer: str = "Bearer"
    basic: str = "Basic"
