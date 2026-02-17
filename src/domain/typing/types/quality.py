# coding utf-8

from typing import TypeVar

from ..enums import VideoQuality

TQuality = TypeVar(
    "TQuality",
    bound=VideoQuality,
)
