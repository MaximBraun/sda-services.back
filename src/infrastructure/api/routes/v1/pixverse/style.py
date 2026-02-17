# coding utf-8

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
)

from ....views.v1 import PixverseStyleView

from ......domain.tools import (
    auto_docs,
    validate_token,
    save_upload_file,
)

from .....factroies.api.v1 import PixverseStyleViewFactory

from ......interface.schemas.api import (
    Style,
    IStyle,
    ChangeStyle,
)


pixverse_style_router = APIRouter(tags=["Styles"])


@pixverse_style_router.get(
    "/styles",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/styles",
    "GET",
    description="Роутер для получения объектов.",
)
async def fetch_styles(
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> list[Style]:
    return await view.fetch_styles(
        token_data,
    )


@pixverse_style_router.get(
    "/styles/{id}",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/styles/{id}",
    "GET",
    params={
        "id": {
            "type": "integer",
            "description": "Уникальный идентификатор объекта из базы данных",
        }
    },
    description="Роутер для получения объекта по уникальному идентификатору из базы данных",
)
async def fetch_style_by_id(
    id: int,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> Style:
    return await view.fetch_style_by_id(
        id,
        token_data,
    )


@pixverse_style_router.post(
    "/styles",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/styles",
    "POST",
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
    description="Роутер для нового создания объекта",
)
async def add_style(
    data: IStyle = Depends(),
    preview_small: UploadFile | None = None,
    preview_large: UploadFile | None = None,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> ChangeStyle:
    return await view.add_style(
        data,
        save_upload_file(preview_small, subdir="video/small"),
        save_upload_file(preview_large, subdir="video/large"),
        token_data,
    )


@pixverse_style_router.put(
    "/styles/{id}",
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
async def update_style(
    id: int,
    data: IStyle = Depends(),
    preview_small: UploadFile | None = None,
    preview_large: UploadFile | None = None,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> ChangeStyle:
    return await view.update_style(
        id,
        data,
        save_upload_file(preview_small, subdir="small"),
        save_upload_file(preview_large, subdir="large"),
        token_data,
    )


@pixverse_style_router.delete(
    "/styles/{id}",
    include_in_schema=False,
)
@auto_docs(
    "api/v1/styles/{id}",
    "DELETE",
    params={
        "id": {
            "type": "string",
            "description": "Уникальный идентификатор объекта",
        },
    },
    description="Роутер для удаления созданного стиля по идентификатору",
)
async def delete_style(
    id: int,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PixverseStyleView = Depends(PixverseStyleViewFactory.create),
) -> bool:
    return await view.delete_style(
        id,
        token_data,
    )
