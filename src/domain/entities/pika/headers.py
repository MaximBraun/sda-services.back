# coding utf-8

from typing import Annotated

from pydantic import Field, field_validator

from ..core import ISchema


class ITokenHeaders(ISchema):
    token: Annotated[
        str | None,
        Field(default=None, alias="Authorization"),
    ]
    """JWT ключ для API"""

    api_key: Annotated[
        str | None,
        Field(default=None, alias="ApiKey"),
    ]

    cookie: Annotated[
        str | None,
        Field(default=None, alias="Cookie"),
    ]

    next_action: Annotated[
        str,
        Field(default="a4f7d00566d7755f69cb53e2b2bbaf32236f107e", alias="Next-Action"),
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
