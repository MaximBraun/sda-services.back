# coding utf-8

from typing import Annotated

from pydantic import Field

from ..core import ISchema


class ITokenHeaders(ISchema):
    cookie: Annotated[
        str | None,
        Field(default=None, alias="Cookie"),
    ]
