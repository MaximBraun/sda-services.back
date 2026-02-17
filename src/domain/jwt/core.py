# coding: utf-8

from typing import (
    Any,
    Type,
    get_args,
)

from jwt import encode

from functools import cached_property

from ..entities.core import IConfEnv

from ..entities.auth import (
    UserAuthToken,
    RefreshToken,
    AccessToken,
)

from ..conf import app_conf


conf: IConfEnv = app_conf()


class AuthTokenService:
    def __init__(
        self,
        conf: IConfEnv = conf,
    ) -> None:
        self._conf = conf

    @cached_property
    def secret_key(
        self,
    ) -> str:
        return self._conf.secret_key

    @cached_property
    def algorithm(
        self,
    ) -> str:
        return self._conf.algorithm

    def __call__(
        self,
        *args,
        **kwargs,
    ) -> UserAuthToken:
        token_data = self.generate_auth_token(
            *args,
            **kwargs,
        )
        return UserAuthToken(
            **token_data,
        )

    def encode_token(
        self,
        token: Type[AccessToken | RefreshToken],
    ) -> str:
        return encode(
            token.model_dump(
                by_alias=True,
                exclude_none=True,
            ),
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def generate_auth_token(
        self,
        user_data: dict[str, Any],
        schemas: Any,
    ) -> dict[Type[AccessToken | RefreshToken], Any]:
        return dict(
            map(
                lambda token: (
                    token.model_config.get("title"),
                    self.encode_token(
                        token(**user_data.__dict__),
                    ),
                ),
                get_args(schemas),
            )
        )


app_auth = AuthTokenService()
