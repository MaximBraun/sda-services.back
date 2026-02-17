# coding utf-8

from .pixverse import (
    PixVerseViewFactory,
    PixverseTemplateViewFactory,
    PixverseAccountViewFactory,
    PixverseStyleViewFactory,
    PixverseApplicationViewFactory,
    UserDataViewFactory,
)

from .auth import AuthUserViewFactory

from .chatgpt import (
    ChatGPTViewFactory,
    PhotoGeneratorApplicationViewFactory,
    PhotoGeneratorTemplateViewFactory,
)

from .calories import CaloriesViewFactory

from .common import (
    ApplicationViewFactory,
    ProductViewFactory,
)

from .instagram import InstagramViewFactory

from .cosmetic import CosmeticViewFactory

from .topmedia import (
    TopmediaViewFactory,
    TopmediaVoiceViewFactory,
)

from .qwen import (
    QwenViewFactory,
    QwenAccountViewFactory,
)

from .user import (
    UserServiceViewFactory,
    UserRouteViewFactory,
)

from .pika import (
    PikaViewFactory,
    PikaTemplateViewFactory,
    PikaAccountViewFactory,
    PikaApplicationViewFactory,
)

from .wan import WanViewFactory

from .ximilar import XimilarViewFactory

__all__: list[str] = [
    "PixVerseViewFactory",
    "PixverseAccountViewFactory",
    "AuthUserViewFactory",
    "PixverseStyleViewFactory",
    "PixverseTemplateViewFactory",
    "PixverseApplicationViewFactory",
    "UserDataViewFactory",
    "ChatGPTViewFactory",
    "PhotoGeneratorApplicationViewFactory",
    "PhotoGeneratorTemplateViewFactory",
    "CaloriesViewFactory",
    "ApplicationViewFactory",
    "InstagramViewFactory",
    "ProductViewFactory",
    "CosmeticViewFactory",
    "TopmediaViewFactory",
    "TopmediaVoiceViewFactory",
    "QwenViewFactory",
    "UserServiceViewFactory",
    "UserRouteViewFactory",
    "PikaViewFactory",
    "PikaTemplateViewFactory",
    "PikaApplicationViewFactory",
    "PikaAccountViewFactory",
    "WanViewFactory",
    "QwenAccountViewFactory",
    "XimilarViewFactory",
]
