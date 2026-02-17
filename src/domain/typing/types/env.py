# coding utf-8

from typing import TypeVar

from ..enums import ConfEnv


TConf = TypeVar(
    "TConf",
    bound=ConfEnv,
)
