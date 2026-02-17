# coding utf-8

from typing import Annotated, Any

from pydantic import Field

from .base import ISchema


class ITask(ISchema):
    task: Annotated[
        str,
        Field(...),
    ]
    schedule: Annotated[
        Any,
        Field(...),
    ]
