# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
)

from ....views.v1 import PhotoGeneratorTemplateView

from ......domain.tools import (
    auto_docs,
    validate_token,
    save_upload_file,
)
from .....factroies.api.v1 import PhotoGeneratorTemplateViewFactory

from ......interface.schemas.api import (
    Template,
    ITemplate,
    ChangeTemplate,
)


photo_generator_template_router = APIRouter(tags=["Templates"])


@photo_generator_template_router.get(
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
    view: PhotoGeneratorTemplateView = Depends(
        PhotoGeneratorTemplateViewFactory.create
    ),
) -> list[Template]:
    return await view.fetch_templates(
        token_data,
    )


@photo_generator_template_router.get(
    "/templates/{template_id}",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/templates/{template_id}",
    "GET",
    params={
        "template_id": {
            "type": "integer",
            "description": "Уникальный идентификатор объекта",
        }
    },
    description="Роутер для получения объекта по уникальному идентификатору",
)
async def fetch_template_by_template_id(
    template_id: int,
    view: PhotoGeneratorTemplateView = Depends(
        PhotoGeneratorTemplateViewFactory.create
    ),
) -> Template:
    return await view.fetch_template_by_template_id(
        template_id,
    )


@photo_generator_template_router.get(
    "/templates/{id}",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/templates/{id}",
    "GET",
    params={
        "id": {
            "type": "integer",
            "description": "Уникальный идентификатор объекта из базы данных",
        }
    },
    description="Роутер для получения объекта по уникальному идентификатору из базы данных",
)
async def fetch_template_by_id(
    id: int,
    view: PhotoGeneratorTemplateView = Depends(
        PhotoGeneratorTemplateViewFactory.create
    ),
) -> Template:
    return await view.fetch_template_by_id(
        id,
    )


@photo_generator_template_router.post(
    "/templates",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/templates",
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
async def add_template(
    data: ITemplate = Depends(),
    preview_small: UploadFile | None = None,
    preview_large: UploadFile | None = None,
    _: str = Depends(validate_token),
    view: PhotoGeneratorTemplateView = Depends(
        PhotoGeneratorTemplateViewFactory.create
    ),
) -> ChangeTemplate:
    return await view.add_template(
        data,
        save_upload_file(preview_small, subdir="photo/small"),
        save_upload_file(preview_large, subdir="photo/large"),
    )


@photo_generator_template_router.put(
    "/templates/{id}",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/styles/{id}",
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
async def update_template(
    id: int,
    data: ITemplate = Depends(),
    preview_small: UploadFile | None = None,
    preview_large: UploadFile | None = None,
    _: str = Depends(validate_token),
    view: PhotoGeneratorTemplateView = Depends(
        PhotoGeneratorTemplateViewFactory.create
    ),
) -> ChangeTemplate:
    return await view.update_template(
        id,
        data,
        save_upload_file(preview_small, subdir="small"),
        save_upload_file(preview_large, subdir="large"),
    )


@photo_generator_template_router.delete(
    "/templates/{id}",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/templates/{id}",
    "DELETE",
    params={
        "id": {
            "type": "string",
            "description": "Уникальный идентификатор объекта",
        },
    },
    description="Роутер для удаления созданного стиля по идентификатору",
)
async def delete_template(
    id: int,
    _: str = Depends(validate_token),
    view: PhotoGeneratorTemplateView = Depends(
        PhotoGeneratorTemplateViewFactory.create
    ),
) -> bool:
    return await view.delete_template(
        id,
    )
