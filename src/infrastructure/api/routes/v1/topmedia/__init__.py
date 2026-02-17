# coding utf-8

from .topmedia import topmedia_router

from .voice import topmedia_voice_router

__all__: list[str] = [
    "topmedia_router",
    "topmedia_voice_router",
]
