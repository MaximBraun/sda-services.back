# coding utf-8

from typing import (
    Annotated,
    NamedTuple,
)

from uuid import uuid4

from json import loads

from pendulum import now

from fastapi import UploadFile

from pydantic import (
    Field,
    field_validator,
    model_validator,
)

from ....domain.entities.core import ISchema


class UploadIMG(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    size: Annotated[
        int,
        Field(...),
    ]
    path: Annotated[
        str,
        Field(...),
    ]


class IPixverseBody(ISchema):
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]
    app_id: Annotated[
        str,
        Field(..., alias="appId"),
    ]


class ITopmediaBody(IPixverseBody):
    app_id: Annotated[
        str,
        Field(..., alias="app_bundle_id"),
    ]


class T2VBody(IPixverseBody):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]


class I2VBody(IPixverseBody):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]


class R2VBody(IPixverseBody):
    template_id: Annotated[
        str | None,
        Field(default=None, alias="templateId"),
    ]


class TE2VBody(IPixverseBody):
    template_id: Annotated[
        str | None,
        Field(default=None, alias="templateId"),
    ]


class IMGBody(ISchema):
    images: list[UploadIMG]


class VideoBody(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    path: Annotated[
        str,
        Field(...),
    ]
    type: Annotated[
        int,
        Field(default=1),
    ]

    @field_validator("path", mode="after")
    @classmethod
    def validate_image_path(
        cls,
        value: str,
    ) -> str:
        return "".join(("upload/", value))


class Filter(ISchema):
    off_peak: Annotated[
        int,
        Field(default=0),
    ]


class StatusBody(ISchema):
    offset: Annotated[
        int,
        Field(default=0),
    ]
    limit: Annotated[
        int,
        Field(default=50),
    ]
    filter: Annotated[
        Filter,
        Field(default=Filter()),
    ]
    web_offset: Annotated[
        int,
        Field(default=0),
    ]
    app_offset: Annotated[
        int,
        Field(default=0),
    ]


class GenBody(ISchema):
    video_id: Annotated[
        int,
        Field(...),
    ]


class TemplateBody(ISchema):
    offset: Annotated[
        int,
        Field(default=0),
    ]
    limit: Annotated[
        int,
        Field(default=100),
    ]


class GenerationData(ISchema):
    uuid: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    generation_id: Annotated[
        int | str | None,
        Field(default=None),
    ]
    account_id: Annotated[
        int | None,
        Field(default=None),
    ]
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    app_name: Annotated[
        str,
        Field(...),
    ]
    generation_url: Annotated[
        str | None,
        Field(default=None),
    ]


class UsrData(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    app_id_usage: Annotated[
        int,
        Field(default=1),
    ]


class UserUpdateData(UsrData):
    balance: Annotated[
        int,
        Field(...),
    ]


class UserEventData(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(..., alias="bundle_id"),
    ]
    product_id: Annotated[
        str,
        Field(...),
    ]
    created_at: Annotated[
        str,
        Field(default_factory=lambda: str(now())),
    ]


class UserToken(ISchema):
    account_id: Annotated[
        int,
        Field(...),
    ]
    jwt_token: Annotated[
        str | None,
        Field(default=None),
    ]
    api_key: Annotated[
        str | None,
        Field(default=None),
    ]
    user_id: Annotated[
        str | None,
        Field(default=None),
    ]
    cookies: Annotated[
        str | None,
        Field(default=None),
    ]


class AccountInfo(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    username: Annotated[
        str,
        Field(...),
    ]


class UserStatistics(ISchema):
    id: Annotated[
        int,
        Field(...),
    ]
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    balance: Annotated[
        int,
        Field(...),
    ]
    app_id_usage: Annotated[
        int,
        Field(...),
    ]
    generation_ids: Annotated[
        list[int | str],
        Field(...),
    ]
    accounts: Annotated[
        list[AccountInfo],
        Field(...),
    ]


class UserFilters(ISchema):
    user_ids: Annotated[
        list[str],
        Field(...),
    ]
    app_ids: Annotated[
        list[str],
        Field(...),
    ]


class IInstagramUser(ISchema):
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]
    app_id: Annotated[
        str,
        Field(..., alias="appId"),
    ]


class T2PBody(IInstagramUser):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]


class InstagramAuthUser(IInstagramUser):
    password: Annotated[
        str,
        Field(...),
    ]
    verification_code: Annotated[
        str | None,
        Field(default=None),
    ]

    @classmethod
    def exclude_fields(cls) -> set[str]:
        return {
            "user_id",
            "app_id",
            "search_user",
        }


class UserRelationStats(NamedTuple):
    follower_usernames: set[str]
    followee_usernames: set[str]
    mutual_usernames: set[str]
    not_following_back: set[str]
    not_followed_by: set[str]

    @property
    def mutual_count(self) -> int:
        return len(self.mutual_usernames)

    @property
    def not_following_back_count(self) -> int:
        return len(self.not_following_back)

    @property
    def not_followed_by_count(self) -> int:
        return len(self.not_followed_by)


class PikaAccountData(ISchema):
    token: Annotated[
        str,
        Field(...),
    ]
    api_key: Annotated[
        str,
        Field(...),
    ]
    user_id: Annotated[
        str,
        Field(...),
    ]
    cookies: Annotated[
        str,
        Field(...),
    ]


class PikaT2VBody(ISchema):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "PikaT2VBody":
        if isinstance(values, str):
            return loads(values)
        return values


class PikaV2VBody(ISchema):
    template_id: Annotated[
        str,
        Field(..., alias="templateId"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "PikaT2VBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IMediaFileData(ISchema):
    bytes: Annotated[
        bytes,
        Field(...),
    ]
    ext: Annotated[
        str,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]

    @property
    def filename(
        self,
    ) -> str:
        return f"{self.name}{self.ext}"
