# coding utf-8

from typing import Annotated

from pydantic import Field, field_validator

from ..core import ISchema


class ITokenHeaders(ISchema):
    token: Annotated[
        str | None,
        Field(default=None, alias="Authorization"),
    ]

    @field_validator("token", mode="after")
    @classmethod
    def validate_token(
        cls,
        value: str | None,
    ) -> str | None:
        if value is not None:
            return f"Bearer {value}"
        return value
