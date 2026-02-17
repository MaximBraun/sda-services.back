# coding utf-8

from typing import Annotated

from pydantic import (
    ConfigDict,
    Field,
    field_validator,
)

from pendulum import now

from uuid import uuid4

from ..core import ISchema

from ...typing.types import TToken

from ...typing.enums import (
    TokenTitle,
    TokenType,
    TokenExpiry,
    AuthType,
)


class IToken(ISchema):
    id: Annotated[
        int,
        Field(..., alias="aid"),
    ]
    typ: Annotated[
        TToken,
        Field(...),
    ]
    uuid: Annotated[
        str,
        Field(..., alias="sub"),
    ]
    exp: Annotated[
        int | None,
        Field(default=None),
    ]
    iat: Annotated[
        int,
        Field(default_factory=lambda: int(now().timestamp())),
    ]
    jti: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    role: Annotated[
        str,
        Field(...),
    ]


class AccessToken(IToken):
    typ: Annotated[
        TToken,
        Field(default=TokenType.access),
    ]

    exp: Annotated[
        int,
        Field(
            default_factory=lambda: int(
                now().add(seconds=TokenExpiry.access).timestamp()
            )
        ),
    ]

    model_config: ConfigDict = ConfigDict(
        title=TokenTitle.access,
    )


class RefreshToken(IToken):
    typ: Annotated[
        TToken,
        Field(default=TokenType.refresh),
    ]

    exp: Annotated[
        int,
        Field(
            default_factory=lambda: int(
                now().add(seconds=TokenExpiry.refresh).timestamp()
            )
        ),
    ]

    model_config: ConfigDict = ConfigDict(
        title=TokenTitle.refresh,
    )


class UserAuthToken(ISchema):
    token_type: Annotated[
        str,
        Field(default=AuthType.bearer),
    ]
    access_token: Annotated[
        str,
        Field(...),
    ]
    refresh_token: Annotated[
        str | None,
        Field(default=None),
    ]
