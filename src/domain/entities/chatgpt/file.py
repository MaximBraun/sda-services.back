# coding utf-8

from typing import Annotated

from pydantic import Field

from ..core import ISchema


class IFile(ISchema):
    prompt: Annotated[
        tuple,
        Field(...),
    ]
    model: Annotated[
        tuple,
        Field(...),
    ]
    image: Annotated[
        tuple,
        Field(...),
    ]
