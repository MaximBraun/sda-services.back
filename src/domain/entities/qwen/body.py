# coding utf-8

from typing import Annotated

from json import loads

from pendulum import now

from uuid import uuid4

from hashlib import sha256

from pydantic import (
    Field,
    field_validator,
    model_validator,
)

from ..core import ISchema

from ...constants import MEDIA_SIZES, BODY_AREA


class IQwenAccount(ISchema):
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


class QwenLoginBody(ISchema):
    email: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ) -> str:
        return sha256(value.encode()).hexdigest()


class IQwenChat(ISchema):
    chat_mode: Annotated[
        str,
        Field(default="normal"),
    ]
    chat_type: Annotated[
        str,
        Field(...),
    ]
    models: Annotated[
        list[str],
        Field(default=["qwen3-max-2025-10-30"]),
    ]
    timestamp: Annotated[
        int,
        Field(default_factory=lambda: now().int_timestamp * 1000),
    ]
    title: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]


class IFeatureConfig(ISchema):
    thinking_enabled: Annotated[
        bool,
        Field(default=False),
    ]
    output_schema: Annotated[
        str,
        Field(default="phase"),
    ]


class IQwenFileInfo(ISchema):
    created_at: Annotated[
        int,
        Field(default_factory=lambda: now().int_timestamp * 1000),
    ]
    data: Annotated[
        dict,
        Field(default={}),
    ]
    filename: Annotated[
        str,
        Field(...),
    ]
    hash: Annotated[
        None,
        Field(default=None),
    ]
    id: Annotated[
        str,
        Field(...),
    ]
    user_id: Annotated[
        str,
        Field(...),
    ]
    meta: Annotated[
        dict,
        Field(default={}),
    ]
    update_at: Annotated[
        int,
        Field(default_factory=lambda: now().int_timestamp * 1000),
    ]

    @property
    def dict(
        self,
    ):
        return self.model_dump(
            exclude_none=False,
            by_alias=True,
        )


class IQwenFile(ISchema):
    collection_name: Annotated[
        str,
        Field(default=""),
    ]
    error: Annotated[
        str,
        Field(default=""),
    ]
    file: Annotated[
        IQwenFileInfo,
        Field(...),
    ]
    file_class: Annotated[
        str,
        Field(default="vision"),
    ]
    file_type: Annotated[
        str,
        Field(...),
    ]
    greenNet: Annotated[
        str,
        Field(default="success"),
    ]
    id: Annotated[
        str,
        Field(...),
    ]
    itemId: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    progress: Annotated[
        int,
        Field(default=0),
    ]
    showType: Annotated[
        str,
        Field(default="image"),
    ]
    size: Annotated[
        int,
        Field(...),
    ]
    status: Annotated[
        str,
        Field(default="uploaded"),
    ]
    type: Annotated[
        str,
        Field(default="image"),
    ]
    uploadTaskId: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    url: Annotated[
        str,
        Field(...),
    ]

    @property
    def dict(
        self,
    ):
        return self.model_dump(
            exclude_none=False,
            by_alias=True,
        )


class IQwenChatMessage(ISchema):
    fid: Annotated[
        str,
        Field(default_factory=lambda: str(uuid4())),
    ]
    parent_id: Annotated[
        str | None,
        Field(default=None, alias="parentId"),
    ]
    parent: Annotated[
        str | None,
        Field(default=None, alias="parent_id"),
    ]
    children_ids: Annotated[
        list[str],
        Field(..., alias="childrenIds"),
    ]
    role: Annotated[
        str,
        Field(default="user"),
    ]
    content: Annotated[
        str,
        Field(...),
    ]
    user_action: Annotated[
        str,
        Field(default="chat"),
    ]
    files: Annotated[
        list[IQwenFile],
        Field(default=[]),
    ]
    timestamp: Annotated[
        int,
        Field(default_factory=lambda: now().int_timestamp * 1000),
    ]
    models: Annotated[
        list[str],
        Field(default_factory=lambda: ["qwen3-max-2025-10-30"]),
    ]
    chat_type: Annotated[
        str,
        Field(...),
    ]
    sub_chat_type: Annotated[
        str | None,
        Field(default=None),
    ]
    feature_config: Annotated[
        IFeatureConfig,
        Field(default_factory=IFeatureConfig),
    ]
    extra: Annotated[
        dict[str, dict[str, str]],
        Field(default={}),
    ]

    @model_validator(mode="before")
    def populate_sub_chat_and_extra(
        cls,
        values: dict[str, str | dict[str, ...]],
    ):
        chat_type = values.get("chat_type")

        values.setdefault(
            "sub_chat_type",
            chat_type,
        )
        extra = values.get("extra", {})

        extra.setdefault("meta", {})["subChatType"] = values["sub_chat_type"]
        values["extra"] = extra
        return values

    @property
    def dict(
        self,
    ):
        return self.model_dump(
            exclude_none=False,
            by_alias=True,
        )


class IQwenPhotoBody(ISchema):
    chat_id: Annotated[
        str,
        Field(...),
    ]
    chat_mode: Annotated[
        str,
        Field(default="normal"),
    ]
    incremental_output: Annotated[
        bool,
        Field(default=True),
    ]
    messages: Annotated[
        list[IQwenChatMessage],
        Field(...),
    ]
    model: Annotated[
        str,
        Field(default="qwen3-max-2025-10-30"),
    ]
    parent_id: Annotated[
        str | None,
        Field(default=None),
    ]
    stream: Annotated[
        bool,
        Field(default=False),
    ]
    timestamp: Annotated[
        int,
        Field(default_factory=lambda: now().int_timestamp),
    ]
    size: Annotated[
        str,
        Field(default="1:1"),
    ]

    @property
    def dict(
        self,
    ):
        return self.model_dump(
            exclude_none=False,
            by_alias=True,
        )


class IQwenStatus(ISchema):
    aemPageId: Annotated[
        str,
        Field(default="//chat.qwen.ai/c/"),
    ]
    cdn_version: Annotated[
        str,
        Field(default="0.0.203"),
    ]
    domain: Annotated[
        str,
        Field(default="chat.qwen.ai"),
    ]
    orgid: Annotated[
        str,
        Field(default="tongyi"),
    ]
    spmId: Annotated[
        str,
        Field(default="a2ty_o01.29997173"),
    ]
    typarm1: Annotated[
        str,
        Field(default="web"),
    ]
    typarm2: Annotated[
        str,
        Field(...),
    ]
    typarm3: Annotated[
        str,
        Field(default="prod"),
    ]
    typarm4: Annotated[
        str,
        Field(default="qwen_chat"),
    ]
    typarm5: Annotated[
        str,
        Field(default="product"),
    ]


class IQwenStatusBody(ISchema):
    typarms: Annotated[
        IQwenStatus,
        Field(...),
    ]


class IT2IBody(ISchema):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]
    media_size: Annotated[
        MEDIA_SIZES,
        Field(default="16:9", alias="mediaSize"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IT2IBody":
        if isinstance(values, str):
            return loads(values)
        return values


class II2RBody(ISchema):
    area: Annotated[
        BODY_AREA,
        Field(default="waist"),
    ]
    strength: Annotated[
        float,
        Field(...),
    ]
    media_size: Annotated[
        MEDIA_SIZES,
        Field(default="16:9"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "II2RBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IT2TBody(ISchema):
    media_size: Annotated[
        MEDIA_SIZES,
        Field(default="16:9"),
    ]
    template_id: Annotated[
        int,
        Field(..., alias="id"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IT2TBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IP2BBody(ISchema):
    media_size: Annotated[
        MEDIA_SIZES,
        Field(default="16:9"),
    ]
    box_name: Annotated[
        str,
        Field(...),
    ]
    template_id: Annotated[
        int | None,
        Field(default=None, alias="id"),
    ]
    box_color: Annotated[
        str | None,
        Field(default=None),
    ]
    in_box: Annotated[
        str | None,
        Field(default=None),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IP2BBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IT2CBody(ISchema):
    description: Annotated[
        str,
        Field(...),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IT2TBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IPhotoBody(ISchema):
    filename: Annotated[
        str,
        Field(default_factory=lambda: f"{str(uuid4())}.jpg"),
    ]
    filesize: Annotated[
        int,
        Field(...),
    ]
    filetype: Annotated[
        str,
        Field(default="image"),
    ]


class IIT2IBody(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    media_size: Annotated[
        MEDIA_SIZES,
        Field(default="16:9"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IT2IBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IT2PBody(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IT2PBody":
        if isinstance(values, str):
            return loads(values)
        return values
