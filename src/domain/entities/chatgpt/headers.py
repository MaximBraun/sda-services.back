# coding utf-8

from typing import Annotated

from pydantic import (
    Field,
)

from ...conf import app_conf

from ..core import ISchema, IConfEnv


conf: IConfEnv = app_conf()


class IAuthHeaders(ISchema):
    authorzation: Annotated[
        str | None,
        Field(
            default_factory=lambda: f"Bearer {conf.chatgpt_token}",
            alias="Authorization",
        ),
    ]
