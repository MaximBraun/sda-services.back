# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import PikaApplicationView

from ......domain.tools import (
    auto_docs,
    validate_token,
)
from .....factroies.api.v1 import PikaApplicationViewFactory

from ......interface.schemas.api import (
    Application,
)


pika_application_router = APIRouter(tags=["Applications"])


@pika_application_router.get(
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
    view: PikaApplicationView = Depends(PikaApplicationViewFactory.create),
) -> list[Application]:
    return await view.fetch_applications(
        token_data,
    )


@pika_application_router.get(
    "/applications/{app_id}",
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
    view: PikaApplicationView = Depends(PikaApplicationViewFactory.create),
) -> Application | None:
    return await view.fetch_application_by_app_id(
        app_id,
    )
