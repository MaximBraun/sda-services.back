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

from ....infrastructure.orm.database.models import PixverseTemplates

app_service: str = f"/{getenv('APP_SERVICE', 'default')}"

conf: IConfEnv = app_conf()


class ITemplate(ISchema):
    prompt: Annotated[
        str | None,
        Field(default=None),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    category: Annotated[
        str | None,
        Field(default=None),
    ]
    is_active: Annotated[
        bool,
        Field(default=True),
    ]

    @field_validator("name", "category", mode="before")
    @classmethod
    def validate_app_id(
        cls,
        value: str,
    ) -> str:
        return " ".join(value.split())


class ChangeTemplate(ITemplate):
    preview_small: Annotated[
        str | None,
        Field(default=None),
    ]
    preview_large: Annotated[
        str | None,
        Field(default=None),
    ]


class AddTemplate(ITemplate):
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


class Template(ChangeTemplate):
    id: Annotated[
        int,
        Field(...),
    ]
    template_id: Annotated[
        int | str | None,
        Field(default=None),
    ]

    @field_validator("preview_small", "preview_large", mode="after")
    @classmethod
    def create_preview_url(cls, value: str) -> str:
        if not value:
            return value

        if value.startswith("uploads/"):
            relative_path = value.removeprefix("uploads/")
            return (
                f"{conf.domain_url}{app_service}{conf.api_prefix}/media/{relative_path}"
            )

        return value

    @classmethod
    def create(
        cls,
        templates: list[PixverseTemplates],
    ) -> list["Template"]:
        return list(
            map(
                lambda template: cls.model_validate(template),
                templates,
            ),
        )
