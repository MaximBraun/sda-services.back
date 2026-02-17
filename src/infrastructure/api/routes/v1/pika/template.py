# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import PikaTemplateView

from ......domain.tools import (
    auto_docs,
    validate_token,
)
from .....factroies.api.v1 import PikaTemplateViewFactory

from ......interface.schemas.api import (
    Template,
)


pika_template_router = APIRouter(tags=["Templates"])


@pika_template_router.get(
    "/templates",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/templates",
    "GET",
    description="Роутер для получения объектов.",
)
async def fetch_templates(
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PikaTemplateView = Depends(PikaTemplateViewFactory.create),
) -> list[Template]:
    return await view.fetch_templates(
        token_data,
    )
