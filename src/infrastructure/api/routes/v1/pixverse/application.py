# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import PixverseApplicationView

from ......domain.tools import (
    auto_docs,
    validate_token,
)
from .....factroies.api.v1 import PixverseApplicationViewFactory

from ......interface.schemas.api import (
    Application,
    PixverseApplication,
    ChangeApplication,
)


pixverse_application_router = APIRouter(tags=["Applications"])


@pixverse_application_router.get(
    "/applications",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/applications",
    "GET",
    description="Роутер для получения объектов.",
)
async def fetch_applications(
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseApplicationView = Depends(PixverseApplicationViewFactory.create),
) -> list[Application]:
    return await view.fetch_applications(
        token_data,
    )


@pixverse_application_router.get(
    "/get_templates/{app_id}",
    response_model_exclude_none=True,
    # include_in_schema=False,
)
@auto_docs(
    "api/v1/get_templates/{app_id}",
    "GET",
    params={
        "app_id": {
            "type": "string",
            "description": "Уникальное название приложения из базы данных",
        }
    },
    description="Роутер для получения шаблонов по уникальному названию приложения из базы данных",
)
async def get_templates_by_app_id(
    app_id: str,
    view: PixverseApplicationView = Depends(PixverseApplicationViewFactory.create),
) -> Application | None:
    return await view.fetch_application_by_app_id(
        app_id,
    )


@pixverse_application_router.post(
    "/applications",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/applications",
    "POST",
    params={
        "template_id": {
            "type": "integer",
            "description": "Уникальный идентификатор для объекта",
        },
        "prompt": {
            "type": "string",
            "description": "Сообещние для создания генерации",
        },
        "name": {
            "type": "string",
            "description": "Указанное имя для созданого объекта",
        },
        "preview_small": {
            "type": "string",
            "description": "Маленькая фотография для объекта",
        },
        "preview_large": {
            "type": "string",
            "description": "Большая фотография для объекта",
        },
    },
    description="Роутер для нового создания объекта",
)
async def add_application(
    data: PixverseApplication,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseApplicationView = Depends(PixverseApplicationViewFactory.create),
) -> PixverseApplication:
    return await view.add_application(
        data,
        token_data,
    )


@pixverse_application_router.put(
    "/applications/{id}",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/applications/{id}",
    "PUT",
    params={
        "prompt": {
            "type": "string",
            "description": "Сообещние для создания генерации",
        },
        "name": {
            "type": "string",
            "description": "Указанное имя для созданого объекта",
        },
        "preview_small": {
            "type": "string",
            "description": "Маленькая фотография для объекта",
        },
        "preview_large": {
            "type": "string",
            "description": "Большая фотография для объекта",
        },
    },
    description="Роутер для измененния созданного стиля",
)
async def update_application(
    id: int,
    data: ChangeApplication,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseApplicationView = Depends(PixverseApplicationViewFactory.create),
) -> PixverseApplication:
    return await view.update_application(
        id,
        data,
        token_data,
    )


@pixverse_application_router.delete(
    "/applications/{id}",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/applications/{id}",
    "DELETE",
    params={
        "id": {
            "type": "string",
            "description": "Уникальный идентификатор объекта",
        },
    },
    description="Роутер для удаления созданного стиля по идентификатору",
)
async def delete_application(
    id: int,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseApplicationView = Depends(PixverseApplicationViewFactory.create),
) -> bool:
    return await view.delete_application(
        id,
        token_data,
    )
