# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Request,
    Depends,
    File,
)


from ....views.v1 import PixVerseView

from ......domain.tools import (
    auto_docs,
    check_user_tokens,
)

from ......interface.schemas.external import (
    T2VBody,
    I2VBody,
    R2VBody,
    Resp,
    GenerationStatus,
    TE2VBody,
)

from .....factroies.api.v1 import PixVerseViewFactory


pixverse_router = APIRouter(tags=["Pixverse"])


@pixverse_router.post(
    "/text2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/text2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
    },
)
@check_user_tokens(method_cost=20)
async def text_to_video(
    request: Request,
    body: T2VBody = Depends(),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    """
    Генерирует видео на основе текстового запроса.

    Аргументы:
        body (IBody): Тело запроса, содержащее текст (prompt) и дополнительные параметры.
        token (str): OAuth2 access token для авторизации пользователя.
        view (PixVerseView): Зависимость, обрабатывающая бизнес-логику генерации видео.

    Возвращает:
        ResponseModel: Ответ с данными о результате генерации видео.
    """
    return await view.text_to_video(
        body,
    )


@pixverse_router.post(
    "/image2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/image2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "image": {
            "type": "bytes",
            "description": "Фотография для обработки. Максимальный размер 4000х4000.",
        },
    },
)
@check_user_tokens(method_cost=20)
async def image_to_video(
    request: Request,
    body: I2VBody = Depends(),
    image: UploadFile = File(...),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.image_to_video(
        body,
        image,
    )


@pixverse_router.post(
    "/video2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/video2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "templateId": {
            "type": "integer",
            "description": "Уникальный идентификатор стиля c платформы Pixverse (поле в базе template_id).",
        },
        "video": {
            "type": "bytes",
            "description": "Видео-фрагмент для обработки. Максимальный размер 1920х1920.",
        },
    },
)
@check_user_tokens(method_cost=60)
async def restyle_video(
    request: Request,
    body: R2VBody = Depends(),
    video: UploadFile = File(...),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.restyle_video(
        body,
        video,
    )


@pixverse_router.post(
    "/template2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/template2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "templateId": {
            "type": "integer",
            "description": "Уникальный идентификатор стиля c платформы Pixverse (поле в базе template_id).",
        },
        "images": {
            "type": "bytes",
            "description": "Фотография для обработки. Максимальный размер 4000х4000.",
        },
    },
)
@check_user_tokens(method_cost=20)
async def template_video(
    request: Request,
    body: TE2VBody = Depends(),
    image: UploadFile = File(...),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.template_video(
        body,
        image,
    )


@pixverse_router.post(
    "/extend2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/extend2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "video": {
            "type": "bytes",
            "description": "Видео для обработки.",
        },
    },
)
@check_user_tokens(method_cost=40)
async def extend_to_video(
    request: Request,
    body: I2VBody = Depends(),
    video: UploadFile = File(...),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.extend_to_video(
        body,
        video,
    )


@pixverse_router.post(
    "/transition2video",
    response_model=Resp,
    response_model_exclude_none=True,
)
@auto_docs(
    "api/v1/transition2video",
    "POST",
    description="Роутер для создания видео по загруженой фотографии и параметрам.",
    params={
        "promt": {
            "type": "string",
            "description": "Текст для создания видео фрагмента",
        },
        "userId": {
            "type": "string",
            "description": "Уникальный идентификатор пользователя",
        },
        "appId": {
            "type": "string",
            "description": "Уникальный идентификатор приложения",
        },
        "images": {
            "type": "list[bytes]",
            "description": "Фотогорафии для обработки",
        },
    },
)
@check_user_tokens(method_cost=40)
async def transition_to_video(
    request: Request,
    body: I2VBody = Depends(),
    images: list[UploadFile] = File(...),
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> Resp:
    return await view.transition_to_video(
        body,
        images,
    )


@pixverse_router.get(
    "/status",
)
@auto_docs(
    "api/v1/status?id={id}",
    "POST",
    description="Роутер для получения статуса генерации.",
    params={
        "id": {
            "type": "integer",
            "description": "Уникальный индефикатор генерации.",
        },
    },
)
async def generation_status(
    request: Request,
    id: int,
    view: PixVerseView = Depends(PixVerseViewFactory.create),
) -> GenerationStatus:
    """
    Получение текущего статуса генерации видео.

    Аргументы:
        body (GenBody): Тело запроса с параметрами генерации.
            Обязательные поля:
            - video_id (int): Уникальный идентификатор задачи генерации
        token (str): OAuth2 токен доступа для аутентификации пользователя.
            Автоматически внедряется через dependency injection.
        view (PixVerseView): Экземпляр обработчика бизнес-логики.
            Автоматически создается через фабрику зависимостей.

    Возвращает:
        GenerationStatus: Объект с информацией о статусе генерации
    """
    return await view.generation_status(
        id,
    )
