# codinng utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class UserCredentials(ISchema):
    username: Annotated[
        str,
        Field(..., alias="Username"),
    ]
    password: Annotated[
        str,
        Field(..., alias="Password"),
    ]


class AccessToken(ISchema):
    access_token: Annotated[
        str,
        Field(...),
    ]
