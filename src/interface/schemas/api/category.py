# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class ICategory(ISchema):
    title: Annotated[
        str,
        Field(...),
    ]


class Category(ICategory):
    id: Annotated[
        int,
        Field(...),
    ]
