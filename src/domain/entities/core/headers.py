# coding utf-8

from typing import Annotated

from pydantic import (
    Field,
)

from ..core import ISchema


class IHeaders(ISchema):
    content_length: Annotated[
        str,
        Field(..., alias="Content-Length"),
    ]
    content_type: Annotated[
        str,
        Field(..., alias="Content-Type"),
    ]
    accept_ranges: Annotated[
        str,
        Field(default="bytes", alias="Accept-Ranges"),
    ]
