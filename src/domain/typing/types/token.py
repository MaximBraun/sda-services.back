# coding utf-8

from typing import TypeVar

from ..enums import TokenType

TToken = TypeVar(
    "TToken",
    bound=TokenType,
)
