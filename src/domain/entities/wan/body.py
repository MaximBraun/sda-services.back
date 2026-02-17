# coding utf-8

from typing import Annotated

from json import loads

from hashlib import sha256

from pydantic import (
    Field,
    model_validator,
    field_validator,
)

from ..core import ISchema


class WanAuthBody(ISchema):
    username: Annotated[
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


class WanCookie(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    value: Annotated[
        str,
        Field(...),
    ]

    def generate_cookie(
        self,
    ) -> str:
        return f"{self.name}={self.value}"


class WanImagePlacePoint(ISchema):
    height: Annotated[
        int,
        Field(default=1024),
    ]
    left: Annotated[
        int,
        Field(default=0),
    ]
    top: Annotated[
        int,
        Field(default=0),
    ]
    width: Annotated[
        int,
        Field(default=1024),
    ]


class WanImageData(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    obj: Annotated[
        str,
        Field(default="obj", alias="objOrBg"),
    ]
    origin_image: Annotated[
        str,
        Field(..., alias="originImage"),
    ]
    place_point: Annotated[
        WanImagePlacePoint,
        Field(default=WanImagePlacePoint(), alias="placePoint"),
    ]
    result_image: Annotated[
        str,
        Field(..., alias="resultImage"),
    ]


class ITaskInput(ISchema):
    sub_type: Annotated[
        str,
        Field(default="basic", alias="subType"),
    ]
    model_version: Annotated[
        str,
        Field(default="2_5", alias="modelVersion"),
    ]
    generation_mode: Annotated[
        str,
        Field(default="imaginative", alias="generationMode"),
    ]
    model_ids: Annotated[
        list,
        Field(default=[], alias="modelIds"),
    ]
    prompt: Annotated[
        str | None,
        Field(default=None),
    ]
    duration: Annotated[
        int | None,
        Field(default=None),
    ]
    video_sound_switch: Annotated[
        str | None,
        Field(default=None, alias="videoSoundSwitch"),
    ]
    ref_images_url_info: Annotated[
        list[WanImageData] | None,
        Field(default=None, alias="refImagesurlsInfo"),
    ]
    base_image: Annotated[
        str | None,
        Field(default=None, alias="baseImage"),
    ]
    resolution: Annotated[
        str,
        Field(default="1280*1280"),
    ]


class IIT2IBody(ISchema):
    deduct_mode: Annotated[
        str,
        Field(default="credit_mode", alias="deductMode"),
    ]
    task_type: Annotated[
        str,
        Field(default="text_to_image", alias="taskType"),
    ]
    task_input: Annotated[
        ITaskInput,
        Field(..., alias="taskInput"),
    ]

    @classmethod
    def generate(
        cls,
        *args,
        **kwargs,
    ) -> "IT2IBody":
        return cls(
            task_input=ITaskInput(
                *args,
                **kwargs,
            ),
        )


class IIT2VBody(IIT2IBody):
    task_type: Annotated[
        str,
        Field(default="text_to_video", alias="taskType"),
    ]
    task_input: Annotated[
        ITaskInput,
        Field(..., alias="taskInput"),
    ]


class III2VBody(IIT2IBody):
    task_type: Annotated[
        str,
        Field(default="image_to_video", alias="taskType"),
    ]
    task_input: Annotated[
        ITaskInput,
        Field(..., alias="taskInput"),
    ]


class II2IBody(IIT2IBody):
    task_type: Annotated[
        str,
        Field(default="image_to_image", alias="taskType"),
    ]
    task_input: Annotated[
        ITaskInput,
        Field(..., alias="taskInput"),
    ]
    create_scene: Annotated[
        str,
        Field(default="chat", alias="createScene"),
    ]


class IIE2VBody(IIT2IBody):
    task_type: Annotated[
        str,
        Field(default="image_to_video_effect", alias="taskType"),
    ]
    task_input: Annotated[
        ITaskInput,
        Field(..., alias="taskInput"),
    ]


class IT2IBody(ISchema):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IIT2IBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IT2ABody(ISchema):
    angle: Annotated[
        str,
        Field(...),
    ]
    pose: Annotated[
        str,
        Field(...),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IIT2IBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IT2VBody(ISchema):
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IT2VBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IE2VBody(ISchema):
    template_id: Annotated[
        str,
        Field(..., alias="templateId"),
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_json_string(
        cls,
        values: str | ISchema,
    ) -> "IE2VBody":
        if isinstance(values, str):
            return loads(values)
        return values


class IIG2MBody(ISchema):
    task_id: Annotated[
        str,
        Field(..., alias="taskId"),
    ]


class IIF2PBody(ISchema):
    file_name: Annotated[
        str | None,
        Field(default=None, alias="fileName"),
    ]
    key: Annotated[
        str | None,
        Field(default=None),
    ]
    task_type: Annotated[
        str,
        Field(default="", alias="taskType"),
    ]


class IIF2UBody(ISchema):
    access_id: Annotated[
        str,
        Field(..., alias="OSSAccessKeyId"),
    ]
    policy: Annotated[
        str,
        Field(...),
    ]
    signature: Annotated[
        str,
        Field(...),
    ]
    key: Annotated[
        str,
        Field(...),
    ]
    dir: Annotated[
        str,
        Field(...),
    ]
