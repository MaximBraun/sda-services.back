# coding utf-8

from .chatgpt import chatgpt_router

from .application import photo_generator_application_router

from .template import photo_generator_template_router

__all__: list[str] = [
    "chatgpt_router",
    "photo_generator_application_router",
    "photo_generator_template_router",
]
