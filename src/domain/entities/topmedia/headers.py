# coding utf-8

from typing import Annotated

from pydantic import Field

from ..core import ISchema


class ITokenHeaders(ISchema):
    token: Annotated[
        str | None,
        Field(default=None, alias="token"),
    ]

    auth: Annotated[
        str | None,
        Field(default=None, alias="authorization"),
    ]
