# coding utf-8

from typing import (
    Annotated,
    Union,
)

from pydantic import Field

from ..core import ISchema

from ...constants import BODY_POST_CREATOR_SYSTEM_PROMPT


class IImageUrl(ISchema):
    url: Annotated[
        str,
        Field(...),
    ]


class IImageContent(ISchema):
    type: Annotated[
        str,
        Field(default="image_url"),
    ]
    image_url: Annotated[
        IImageUrl,
        Field(...),
    ]


class ITextContent(ISchema):
    type: Annotated[
        str,
        Field(default="text"),
    ]
    text: Annotated[
        str,
        Field(...),
    ]


class IMessage(ISchema):
    role: Annotated[
        str,
        Field(...),
    ]
    content: list[Union[str, ITextContent, IImageContent]]


class InstagramChatGPTBody(ISchema):
    model: Annotated[
        str,
        Field(default="gpt-4o"),
    ]
    temperature: Annotated[
        int,
        Field(default=0),
    ]
    top_p: Annotated[
        int,
        Field(default=1),
    ]
    frequency_penalty: Annotated[
        int,
        Field(default=0),
    ]
    presence_penalty: Annotated[
        int,
        Field(default=0),
    ]
    messages: list[IMessage]

    @classmethod
    def generate_post(
        cls,
        prompt: str,
    ) -> "InstagramChatGPTBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_POST_CREATOR_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(text=prompt),
                    ],
                ),
            ],
        )
