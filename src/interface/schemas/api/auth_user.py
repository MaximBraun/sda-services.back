# coding utf-8

from typing import Annotated

from pydantic import (
    Field,
    field_validator,
)

from ....domain.constants import PWD_CONTEXT

from ....domain.entities.core import ISchema

from ....domain.entities.auth import IToken

from ....domain.tools import decode_token


class AuthUserCredentials(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]

    def validate(
        self,
        hashed_password: str,
    ) -> bool:
        return PWD_CONTEXT.verify(
            self.password,
            hashed_password,
        )


class UserRefreshToken(ISchema):
    refresh_token: Annotated[
        str,
        Field(...),
    ]

    def validate(
        self,
    ) -> IToken:
        return IToken(
            **decode_token(
                self.refresh_token,
            ),
        )


class UserAccessToken(ISchema):
    access_token: Annotated[
        str,
        Field(...),
    ]

    def validate(
        self,
    ) -> IToken:
        return IToken(
            **decode_token(
                self.access_token,
            ),
        )


class ServiceRoute(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    title: Annotated[
        str,
        Field(...),
    ]


class UserService(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    title: Annotated[
        str,
        Field(...),
    ]
