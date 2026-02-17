# coding utf-8

from enum import StrEnum


class PixverseEndpoint(StrEnum):
    """Перечисление URI эндпоинтов API сервиса PixVerse.

    Содержит пути к основным конечным точкам API для:
    - Генерации контента по тексту
    - Генерации изображений
    - Загрузки медиафайлов
    - Проверки статуса задач

    Все URI указаны относительно базового URL API.
    """

    AUTH = "/creative_platform/login"
    """
    Проверка статуса выполненной генерации.
    """

    TEXT = "/creative_platform/video/t2v"
    """
    Генерация контента по текстовому описанию.
    """

    IMAGE = "/creative_platform/video/i2v"
    """
    Генерация контента по заданой фотографии.
    """

    UPLOAD_IMAGE = "/creative_platform/media/batch_upload_media"
    """
    Загрузка пользовательских изображений для создания контента по фотографии.
    """

    UPLOAD_VIDEO = "/creative_platform/media/upload"

    LAST_FRAME = "/creative_platform/video/frame/last"

    UPLOAD_TOKEN = "/creative_platform/getUploadToken"
    """
    Загрузка пользовательских изображений для создания контента по фотографии.
    """

    STATUS = "/creative_platform/video/list/personal"
    """
    Проверка статуса выполненной генерации.
    """

    TOKEN = "/creative_platform/user/credits"

    RESTYLE = "/creative_platform/video/extend"

    RESTYLE_TEMPLATE = "/creative_platform/restyle/list"

    TEMPLATES = "/creative_platform/effect/channel/list"

    EXTEND = "/creative_platform/video/extend"

    TRANSITION = "/creative_platform/video/frames"


class ChatGPTEndpoint(StrEnum):
    TEXT = "/v1/images/generations"
    """
    Генерация контента по заданой фотографии.
    """

    PHOTO = "/v1/images/edits"
    """
    Генерация контента по заданой фотографии.
    """

    CHAT = "/v1/chat/completions"
    """
    Генерация контента по заданой фотографии.
    """


class TopmediaEndpoint(StrEnum):
    AUTH = "/account/login"

    SLANG = "/v2/voice/text_slang"

    USER = "/v2/user/info"

    SPEECH = "/v5/voice/tts"

    DOWNLOAD = "/v2/user/audition/download/{id}"

    SONG = "/v2/async/text-to-song"

    RESULT = "/v2/task/results"


class QwenEndpoint(StrEnum):
    AUTH = "/api/v1/auths/signin"

    USER_TOKEN = "/api/v1/auths"

    CHAT = "/api/v2/chats/new"

    GENERATE = "/api/v2/chat/completions?chat_id={chat_id}"

    STATUS = "/api/v2/users/status"

    RESULT = "/api/v2/chats/{chat_id}"

    MEDIA_TOKEN = "/api/v2/files/getstsToken"


class PikaEndpoint(StrEnum):
    V1 = "/v1.5"

    V2 = "/v2"

    EFFECTS = "/pikaffects"

    LOGIN = "/auth/v1/user"

    STATUS = "/my-library"

    BALANCE = "/rest/v1/subscriptions?select=*&user_id=eq.{user_id}"


class SharkEndpoint(StrEnum):
    ABOUT = "/api/v1/maps/3413/public-pois/{id}/?h=0"


class WanEndpoint(StrEnum):
    AUTH = "/wanx/api/public/user/login"

    GENERATION = "/wanx/api/common/imageGen"

    POLICY = "/wanx/api/oss/getPolicy"

    STATUS = "/wanx/api/common/v2/taskResult"

    OSS = "/wanx/api/oss/generateOssUrl"


class XimilarEndpoint(StrEnum):
    AUTH = "/account/v2/login/"

    CARD = "/collectibles/v2/card_id"
