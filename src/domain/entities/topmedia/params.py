# coding utf-8

from typing import Annotated

from hashlib import md5

from pydantic import (
    Field,
    field_validator,
)

from ..core import ISchema


class TopmediaLoginParams(ISchema):
    email: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]
    information_sources: Annotated[
        str,
        Field(default="https://www.topmediai.com"),
    ]
    source_site: Annotated[
        str,
        Field(default="www.topmediai.com"),
    ]
    software_code: Annotated[
        int,
        Field(default=0),
    ]

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ) -> str:
        return md5(value.encode()).hexdigest()


class TopmediaTokenParams(ISchema):
    token: Annotated[
        str,
        Field(...),
    ]


class TopmediaMusicParams(TopmediaTokenParams):
    ids: Annotated[
        list[str] | str,
        Field(...),
    ]

    @field_validator("ids", mode="after")
    @classmethod
    def validate_ids(
        cls,
        value: list[str],
    ) -> str:
        return ",".join(value)
