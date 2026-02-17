# coding utf-8

from typing import Annotated

from pydantic import Field, field_validator

from ..core import ISchema


class IMediatopAccount(ISchema):
    usage_count: Annotated[
        int,
        Field(...),
    ]

    @field_validator("usage_count", mode="after")
    @classmethod
    def validate_usage_count(
        cls,
        value: int,
    ) -> int:
        return value + 1


class TextSlangBody(ISchema):
    accent: Annotated[
        str,
        Field(default="English(US)"),
    ]
    text: Annotated[
        str,
        Field(...),
    ]
    token: Annotated[
        str,
        Field(...),
    ]
    speaker: Annotated[
        str,
        Field(..., alias="voice_id"),
    ]

    @field_validator("text", mode="after")
    @classmethod
    def validate_text(
        cls,
        value: str,
    ) -> str:
        return f"<speak>{value}</speak>"


class IT2SBody(ISchema):
    text: Annotated[
        str,
        Field(...),
    ]
    speaker: Annotated[
        str,
        Field(...),
    ]
    emotion: Annotated[
        str,
        Field(default="Default", alias="emotion_name"),
    ]
    speed: Annotated[
        float | None,
        Field(default=None),
    ]
    stability: Annotated[
        int | None,
        Field(default=None),
    ]
    similarity: Annotated[
        int | None,
        Field(default=None),
    ]
    exaggeration: Annotated[
        int | None,
        Field(default=None),
    ]
    volume: Annotated[
        int | None,
        Field(default=None),
    ]


class ITSGBody(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    lyrics: Annotated[
        str | None,
        Field(default=None),
    ]
    instrumental: Annotated[
        int,
        Field(default=1),
    ]


class TextSpeechBody(TextSlangBody):
    is_cancel: Annotated[
        bool,
        Field(default=True, alias="isCancel"),
    ]
    emotion: Annotated[
        str,
        Field(..., alias="emotion_name"),
    ]
    speed: Annotated[
        float,
        Field(default=0.5),
    ]
    volume: Annotated[
        int,
        Field(default=50),
    ]
    article_title: Annotated[
        str,
        Field(default="Unnamed"),
    ]
    is_audition: Annotated[
        int,
        Field(default=1),
    ]
    pitch: Annotated[
        int,
        Field(default=50),
    ]
    stability: Annotated[
        int,
        Field(default=50),
    ]
    similarity: Annotated[
        int,
        Field(default=95),
    ]
    exaggeration: Annotated[
        int,
        Field(default=0),
    ]
    plan_type: Annotated[
        int,
        Field(default=2),
    ]
    country_code: Annotated[
        str,
        Field(default="BR"),
    ]


class TextMusicBody(ISchema):
    mv: Annotated[
        str,
        Field(default="v4.5"),
    ]
    is_public: Annotated[
        int,
        Field(default=0),
    ]
    instrumental: Annotated[
        int,
        Field(...),
    ]
    action: Annotated[
        str,
        Field(default="custom"),
    ]
    prompt: Annotated[
        str,
        Field(..., alias="style"),
    ]
    lyrics: Annotated[
        str,
        Field(default=""),
    ]
    title: Annotated[
        str | None,
        Field(default=None),
    ]
    token: Annotated[
        str,
        Field(...),
    ]
