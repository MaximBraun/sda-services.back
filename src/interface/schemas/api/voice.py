# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class Voice(ISchema):
    # id: Annotated[
    #     int,
    #     Field(...),
    # ]
    name: Annotated[
        str,
        Field(...),
    ]
    speaker: Annotated[
        str,
        Field(...),
    ]
    avatar_url: Annotated[
        str,
        Field(...),
    ]
    avatar_url_webp: Annotated[
        str,
        Field(...),
    ]
    audition_url: Annotated[
        str,
        Field(...),
    ]
