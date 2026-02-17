# coding utf-8

from typing import Annotated

from pydantic import Field

from .base import ISchema


class IUserData(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    balance: Annotated[
        int,
        Field(...),
    ]
