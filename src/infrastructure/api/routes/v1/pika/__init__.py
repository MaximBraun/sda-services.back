# codiung utf-8

from .pika import pika_router

from .application import pika_application_router

from .template import pika_template_router

from .account import pika_account_router

__all__: list[str] = [
    "pika_router",
    "pika_template_router",
    "pika_application_router",
    "pika_account_router",
]
