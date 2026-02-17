# coding utf-8

from ..core import ISchema

from pydantic import Field

from typing import Annotated


class ISession(ISchema):
    csrftoken: Annotated[
        str,
        Field(...),
    ]
    ds_user_id: Annotated[
        str,
        Field(...),
    ]
    sessionid: Annotated[
        str,
        Field(...),
    ]
