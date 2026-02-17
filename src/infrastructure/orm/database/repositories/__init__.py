# coding utf-8

from .auth import AuthUserRepository

from .pixverse import (
    PixverseAccountRepository,
    PixverseApplicationRepository,
    PixverseStyleRepository,
    PixverseTemplateRepository,
    UserGenerationRepository,
    UserDataRepository,
    PixverseAccountsTokensRepository,
)

from .chatgpt import (
    PhotoGeneratorTemplateRepository,
    PhotoGeneratorApplicationRepository,
)

from .common import (
    ApplicationRepository,
    ProductRepository,
    WebhookRepository,
    UserEventRepository,
    ServiceRepository,
)

from .instagram import (
    InstagramUserRepository,
    InstagramSessionRepository,
    InstagramUserStatsRepository,
    InstagramUserPostsRepository,
    InstagramUserRelationsRepository,
    InstagramTrackingRepository,
)

from .topmedia import (
    TopmediaAccountRepository,
    TopmediaAccountTokenRepository,
    TopmediaVoiceRepository,
)

from .qwen import (
    QwenAccountRepository,
    QwenAccountTokenRepository,
)

from .pika import (
    PikaAccountRepository,
    PikaAccountsTokensRepository,
    PikaTemplateRepository,
    PikaApplicationRepository,
)

from .wan import (
    WanAccountRepository,
    WanAccountsTokensRepository,
    WanApplicationRepository,
    WanTemplateRepository,
)

from .ximilar import (
    XimilarAccountRepository,
    XimilarAccountsTokensRepository,
    XimilarApplicationRepository,
)

__all__: list[str] = [
    "PixverseAccountRepository",
    "PixverseTemplateRepository",
    "PixverseStyleRepository",
    "AuthUserRepository",
    "UserDataRepository",
    "PixverseApplicationRepository",
    "PhotoGeneratorTemplateRepository",
    "PhotoGeneratorApplicationRepository",
    "UserGenerationRepository",
    "PixverseAccountsTokensRepository",
    "ApplicationRepository",
    "ProductRepository",
    "WebhookRepository",
    "InstagramUserRepository",
    "InstagramSessionRepository",
    "InstagramUserStatsRepository",
    "InstagramUserPostsRepository",
    "InstagramUserRelationsRepository",
    "InstagramTrackingRepository",
    "TopmediaAccountRepository",
    "TopmediaAccountTokenRepository",
    "TopmediaVoiceRepository",
    "QwenAccountRepository",
    "QwenAccountTokenRepository",
    "UserEventRepository",
    "ServiceRepository",
    "PikaAccountRepository",
    "PikaAccountsTokensRepository",
    "PikaTemplateRepository",
    "PikaApplicationRepository",
    "WanAccountRepository",
    "WanAccountsTokensRepository",
    "WanApplicationRepository",
    "WanTemplateRepository",
    "XimilarAccountRepository",
    "XimilarAccountsTokensRepository",
    "XimilarApplicationRepository",
]
