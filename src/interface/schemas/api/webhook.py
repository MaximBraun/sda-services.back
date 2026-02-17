# coding utf-8

from typing import Annotated

from pydantic import Field

from uuid import uuid4

from ....domain.entities.core import ISchema


class Webhook(ISchema):
    uuid: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
