# coding utf-8

from typing import Annotated

from os import getenv

from pydantic import (
    Field,
    field_validator,
)

from ....domain.conf import app_conf

from ....domain.entities.core import (
    ISchema,
    IConfEnv,
)

app_service: str = f"/{getenv('APP_SERVICE', 'default')}"

conf: IConfEnv = app_conf()


class IProduct(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    tokens_amount: Annotated[
        int,
        Field(default=0),
    ]
    is_active: Annotated[
        bool,
        Field(default=True),
    ]


class Product(IProduct):
    id: Annotated[
        int,
        Field(...),
    ]
