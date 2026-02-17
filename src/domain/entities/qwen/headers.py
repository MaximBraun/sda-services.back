# coding utf-8

from typing import Annotated

from pydantic import Field, field_validator

from fake_useragent import UserAgent

from uuid import uuid4

from ..core import ISchema


class ITokenHeaders(ISchema):
    token: Annotated[
        str | None,
        Field(default=None, alias="authorization"),
    ]

    user_agent: Annotated[
        str,
        Field(default=UserAgent().random, alias="User-Agent"),
    ]

    accept: Annotated[
        str,
        Field(default="application/json, text/plain, */*", alias="Accept"),
    ]

    accept_language: Annotated[
        str,
        Field(default="en-US,en;q=0.9", alias="Accept-Language"),
    ]

    accept_encoding: Annotated[
        str,
        Field(default="gzip, deflate, br, zstd", alias="Accept-Encoding"),
    ]

    origin: Annotated[
        str,
        Field(default="https://chat.qwen.ai", alias="Origin"),
    ]

    referer: Annotated[
        str,
        Field(default="https://chat.qwen.ai/", alias="Referer"),
    ]

    host: Annotated[
        str,
        Field(default="chat.qwen.ai", alias="Host"),
    ]

    connection: Annotated[
        str,
        Field(default="keep-alive", alias="Connection"),
    ]

    version: Annotated[
        str,
        Field(default="0.0.209", alias="Version"),
    ]

    x_request_id: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4()), alias="X-Request-Id"),
    ]

    cookie: Annotated[
        str,
        Field(
            default="acw_tc=0a03e59117645084970997698e7b96e24abe23f35ff443dad6d09101c10590; x-ap=eu-central-1",
            alias="Cookie",
        ),
    ]

    @field_validator("token", mode="after")
    @classmethod
    def validate_token(
        cls,
        value: str | None,
    ) -> str:
        if value is not None:
            return f"Bearer {value}"
        return value
