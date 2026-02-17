# coding utf-8

from typing import Any

from jwt import (
    decode,
    ExpiredSignatureError,
    DecodeError,
)

from fastapi import Depends, status

from fastapi.security import OAuth2PasswordBearer

from ..conf import app_conf

from ..entities.core import IConfEnv

from ..typing.enums import TokenType

from ..errors import TokenError


conf: IConfEnv = app_conf()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/api/v1/token",
)


def decode_token(
    token: str,
) -> dict[str, Any]:
    try:
        return decode(
            token,
            conf.secret_key,
            algorithms=[conf.algorithm],
        )
    except (ExpiredSignatureError, DecodeError):
        raise TokenError


def validate_token(
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    token_data = decode_token(token)
    if not token_data.get("typ") == TokenType.access:
        raise TokenError
    return token_data
