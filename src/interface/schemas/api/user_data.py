# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class UserData(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
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
    app_id_usage: Annotated[
        int,
        Field(...),
    ]
