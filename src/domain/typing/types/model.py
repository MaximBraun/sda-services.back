# coding utf-8

from typing import TypeVar

from ..enums import ModelVersion

TModel = TypeVar(
    "TModel",
    bound=ModelVersion,
)
