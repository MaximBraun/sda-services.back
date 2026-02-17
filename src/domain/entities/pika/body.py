# coding utf-8

from typing import Annotated, Any

from pydantic import (
    Field,
    field_validator,
    field_serializer,
)

from json import dumps

from ..core import ISchema


class IParameters(ISchema):
    guidance_scale: Annotated[
        int,
        Field(default=12, alias="guidanceScale"),
    ]
    motion: Annotated[
        int,
        Field(default=1),
    ]
    negative_prompt: Annotated[
        str,
        Field(default="", alias="negativePrompt"),
    ]


class IOptions(ISchema):
    aspect: Annotated[
        float,
        Field(default=1.7777777777777777, alias="aspectRatio"),
    ]
    frame: Annotated[
        int,
        Field(default=24, alias="frameRate"),
    ]
    camera: Annotated[
        dict,
        Field(default={}),
    ]
    parameters: Annotated[
        Any,
        Field(default=IParameters().dict),
    ]
    extend: Annotated[
        bool,
        Field(default=False),
    ]


class IT2VBody(ISchema):
    resolution: Annotated[
        str,
        Field(default="1080p"),
    ]
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]
    content: Annotated[
        str,
        Field(default="t2v", alias="contentType"),
    ]
    model: Annotated[
        str,
        Field(default="Turbo"),
    ]
    options: Annotated[
        str,
        Field(default_factory=lambda: f"{dumps(IOptions().dict)}"),
    ]
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]


class IP2VBody(ISchema):
    resolution: Annotated[
        str,
        Field(default="1080p"),
    ]
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]
    content: Annotated[
        str,
        Field(default="i2v", alias="contentType"),
    ]
    model: Annotated[
        str,
        Field(default="1.5"),
    ]
    options: Annotated[
        str,
        Field(default_factory=lambda: f"{dumps(IOptions().dict)}"),
    ]
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]


class IV2TBody(ISchema):
    resolution: Annotated[
        str,
        Field(default="1080p"),
    ]
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]
    content: Annotated[
        str,
        Field(default="redirect", alias="contentType"),
    ]
    mode: Annotated[
        str,
        Field(default="redirect"),
    ]
    model: Annotated[
        str,
        Field(default="Turbo"),
    ]
    options: Annotated[
        str,
        Field(default_factory=lambda: f"{dumps(IOptions().dict)}"),
    ]
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]


class IV2VBody(ISchema):
    resolution: Annotated[
        str,
        Field(default="1080p"),
    ]
    prompt: Annotated[
        str,
        Field(..., alias="promptText"),
    ]
    content: Annotated[
        str,
        Field(default="object", alias="contentType"),
    ]
    model: Annotated[
        str,
        Field(default="Turbo"),
    ]
    options: Annotated[
        str,
        Field(default_factory=lambda: f"{dumps(IOptions().dict)}"),
    ]
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]


class II2GBody(ISchema):
    ids: Annotated[
        list[str],
        Field(...),
    ]


class II2VBody(ISchema):
    pika_ffect: Annotated[
        str,
        Field(..., alias="pikaffect"),
    ]
    content: Annotated[
        str,
        Field(default="t2v", alias="contentType"),
    ]
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]


class IV2SBody(ISchema):
    resolution: Annotated[
        str,
        Field(default="1080p"),
    ]
    modifyRegionRoi: Annotated[
        str,
        Field(default="face"),
    ]
    prompt: Annotated[
        str,
        Field(
            default="use face of the uploaded image and paste it to video.",
            alias="promptText",
        ),
    ]
    content: Annotated[
        str,
        Field(default="pikaswaps", alias="contentType"),
    ]
    model: Annotated[
        str,
        Field(default="Turbo"),
    ]
    options: Annotated[
        str,
        Field(default_factory=lambda: f"{dumps(IOptions().dict)}"),
    ]
    mode: Annotated[
        str,
        Field(default="modifyRegion"),
    ]
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]
