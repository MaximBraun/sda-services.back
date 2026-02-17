# coding utf-8

from typing import Annotated

from os import getenv

from pydantic import (
    Field,
    field_validator,
)

from ....domain.conf import app_conf

from ....domain.entities.core import (
    ISchema,
    IConfEnv,
)

from ....infrastructure.orm.database.models import PixverseStyles


app_service: str = f"/{getenv('APP_SERVICE', 'default')}"

conf: IConfEnv = app_conf()


class IStyle(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    is_active: Annotated[
        bool,
        Field(default=True),
    ]

    @field_validator("name", mode="before")
    @classmethod
    def validate_app_id(
        cls,
        value: str,
    ) -> str:
        return " ".join(value.split())


class ChangeStyle(IStyle):
    preview_small: Annotated[
        str | None,
        Field(default=None),
    ]
    preview_large: Annotated[
        str | None,
        Field(default=None),
    ]


class AddStyle(IStyle):
    preview_small: Annotated[
        str | None,
        Field(default=None),
    ]
    preview_large: Annotated[
        str | None,
        Field(default=None),
    ]
    auth_user_id: Annotated[
        int,
        Field(...),
    ]


class Style(ChangeStyle):
    id: Annotated[
        int,
        Field(...),
    ]
    template_id: Annotated[
        int | None,
        Field(default=None),
    ]

    @field_validator("preview_small", "preview_large", mode="after")
    @classmethod
    def create_preview_url(
        cls,
        value: str,
    ) -> str:
        if value is None:
            return value
        relative_path = value.removeprefix("uploads/")
        return f"{conf.domain_url}{app_service}{conf.api_prefix}/media/{relative_path}"

    @classmethod
    def create(
        cls,
        styles: list[PixverseStyles],
    ) -> list["Style"]:
        return list(
            map(
                lambda style: cls.model_validate(style),
                styles,
            ),
        )
