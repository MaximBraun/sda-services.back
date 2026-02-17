# coding utf-8

from typing import Annotated

from pydantic import (
    Field,
)

from ..core import ISchema


class IClientHeaders(ISchema):
    # user_agent: Annotated[
    #     str,
    #     Field(default="Instagram 219.0.0.12.117 Android", alias="User-Agent"),
    # ]
    csrftoken: Annotated[
        str,
        Field(..., alias="X-CSRFToken"),
    ]
    x_ig_app_id: Annotated[
        str,
        Field(default="936619743392459", alias="X-IG-App-ID"),
    ]
    refer: Annotated[
        str,
        Field(default="https://www.instagram.com/", alias="Referer"),
    ]
    accept: Annotated[
        str,
        Field(default="*/*", alias="Accept"),
    ]
    x_requested_with: Annotated[
        str,
        Field(default="XMLHttpRequest", alias="X-Requested-With"),
    ]
