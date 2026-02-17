# coding utf-8

from .auth import AuthUserController

from .pixverse import (
    PixverseAccountController,
    PixverseApplicationController,
    PixVerseController,
    PixverseStyleController,
    PixverseTemplateController,
    UserDataController,
)

from .chatgpt import (
    ChatGPTController,
    PhotoGeneratorApplicationController,
    PhotoGeneratorTemplateController,
)

from .calories import CaloriesController

from .common import (
    ApplicationController,
    ProductController,
)

from .instagram import InstagramController

from .cosmetic import CosmeticController

from .topmedia import (
    TopmediaController,
    TopmediaVoiceController,
)

from .qwen import (
    QwenController,
    QwenAccountController,
)

from .user import (
    UserServiceController,
    UserRouteController,
)

from .pika import (
    PikaController,
    PikaTemplateController,
    PikaApplicationController,
    PikaAccountController,
)

from .wan import WanController

from .ximilar import XimilarController

__all__: list[str] = [
    "AuthUserController",
    "PixVerseController",
    "PixverseAccountController",
    "PixverseStyleController",
    "PixverseTemplateController",
    "PixverseApplicationController",
    "UserDataController",
    "ChatGPTController",
    "PhotoGeneratorApplicationController",
    "PhotoGeneratorTemplateController",
    "CaloriesController",
    "ApplicationController",
    "InstagramController",
    "ProductController",
    "CosmeticController",
    "TopmediaController",
    "TopmediaVoiceController",
    "QwenController",
    "UserServiceController",
    "UserRouteController",
    "PikaController",
    "PikaApplicationController",
    "PikaTemplateController",
    "PikaAccountController",
    "WanController",
    "QwenAccountController",
    "XimilarController",
]
