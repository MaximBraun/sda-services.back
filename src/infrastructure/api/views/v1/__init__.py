# coding utf-8

from .pixverse import (
    PixVerseView,
    PixverseTemplateView,
    PixverseAccountView,
    PixverseStyleView,
    PixverseApplicationView,
    UserDataView,
)

from .auth import AuthUserView

from .chatgpt import (
    ChatGPTView,
    PhotoGeneratorTemplateView,
    PhotoGeneratorApplicationView,
)

from .calories import CaloriesView

from .common import (
    ApplicationView,
    ProductView,
)

from .instagram import InstagramView

from .cosmetic import CosmeticView

from .topmedia import (
    TopmediaView,
    TopmediaVoiceView,
)

from .qwen import (
    QwenView,
    QwenAccountView,
)

from .user import (
    UserServiceView,
    UserRouteView,
)

from .pika import (
    PikaView,
    PikaTemplateView,
    PikaAccountView,
    PikaApplicationView,
)

from .wan import WanView

from .ximilar import XimilarView

__all__: list[str] = [
    "PixVerseView",
    "PixverseAccountView",
    "AuthUserView",
    "PixverseStyleView",
    "PixverseTemplateView",
    "PixverseApplicationView",
    "UserDataView",
    "ApplicationView",
    "ChatGPTView",
    "PhotoGeneratorTemplateView",
    "PhotoGeneratorApplicationView",
    "CaloriesView",
    "ApplicationView",
    "InstagramView",
    "ProductView",
    "CosmeticView",
    "TopmediaView",
    "TopmediaVoiceView",
    "QwenView",
    "UserServiceView",
    "UserRouteView",
    "PikaView",
    "PikaTemplateView",
    "PikaApplicationView",
    "PikaAccountView",
    "WanView",
    "QwenAccountView",
    "XimilarView",
]
