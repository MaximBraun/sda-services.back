# coding utf-8

from typing import (
    Annotated,
    Union,
    Literal,
    Any,
)

from pydantic import Field

from ..core import ISchema

from ...constants import (
    BODY_CALORIES_SYSTEM_PROMPT,
    BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT,
    BODY_POST_CREATOR_SYSTEM_PROMPT,
    BODY_GEMSTONE_PROMPT,
    BODY_TOYBOX_PROMT,
    BODY_FACT_DAY_PROMPT,
    BODY_FACE_SWAP_PROMPT,
    BODY_HONESTLY_PROMPT,
    NUTRITION_ANALYSIS_PROMPT,
    BODY_ANTIQUES_PROMPT,
)


class IBody(ISchema):
    """Базовое тело запроса для конфигурации AI-модели.

    Содержит обязательные параметры для работы с AI-моделью:
    - Выбор конкретной модели
    - Длительность обработки
    - Текст запроса (промпт)
    - Качество результата

    Наследует все особенности сериализации от ISchema.
    """

    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    prompt: Annotated[
        str,
        Field(...),
    ]


class IQwenBody(IBody):
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]
    app_id: Annotated[
        str,
        Field(..., alias="appId"),
    ]
    prompt: Annotated[
        str | None,
        Field(default=None, exclude=True),
    ]


class PhotoBody(ISchema):
    prompt: Annotated[
        str,
        Field(...),
    ]
    model: Annotated[
        str,
        Field(default="gpt-image-1"),
    ]
    size: Annotated[
        str,
        Field(default="auto"),
    ]


class I2CBody(ISchema):
    user_id: Annotated[
        str,
        Field(..., alias="userId"),
    ]
    app_id: Annotated[
        str,
        Field(..., alias="appId"),
    ]


class T2CBody(I2CBody):
    description: Annotated[
        str,
        Field(...),
    ]


class T2PBody(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    id: Annotated[
        int,
        Field(...),
    ]


class TB2PBody(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    box_name: Annotated[
        str,
        Field(...),
    ]
    id: Annotated[
        int | None,
        Field(default=None),
    ]
    box_color: Annotated[
        str | None,
        Field(default=None),
    ]
    in_box: Annotated[
        str | None,
        Field(default=None),
    ]


class R2PBody(ISchema):
    user_id: Annotated[
        str,
        Field(...),
    ]
    app_id: Annotated[
        str,
        Field(...),
    ]
    area: Annotated[
        Literal["waist", "face"],
        Field(default="face"),
    ]
    strength: Annotated[
        float,
        Field(...),
    ]


class R2PBodyPrompt(ISchema):
    """Schema for generating body retouch prompts."""

    prompt: Annotated[
        str,
        Field(...),
    ]

    @classmethod
    def __resolve_action(
        cls,
        strength: float,
    ) -> tuple[str, int]:
        strength = max(0.0, min(1.0, strength))

        delta = strength - 0.5
        if delta < 0:
            return "slim", int(abs(delta) * 200)
        elif delta > 0:
            return "enhance", int(delta * 200)
        return "keep unchanged", 0

    @classmethod
    def reshape(
        cls,
        area: str,
        strength: float,
    ) -> "R2PBodyPrompt":
        action, percent = cls.__resolve_action(strength)

        prompt = (
            f"Edit the photo:\n"
            f"- {action} the {area} by about {percent}%.\n"
            f"- Preserve natural and realistic appearance without distortion.\n"
            f"- Keep overall body proportions balanced and smooth.\n"
            f"- Do not alter face, arms, legs, chest, or background.\n"
            f"- Ensure the {area} blends harmoniously with the rest of the body.\n"
            f"- Maintain realistic lighting, shadows, curves, and skin texture.\n"
            f"- Avoid artifacts, stretching, or unnatural transitions.\n"
            f"- Result must look seamless and professionally retouched."
        )

        return cls(prompt=prompt)

    @classmethod
    def toybox(
        cls,
        box_color: str,
        in_box: str,
        box_name: str,
    ) -> "R2PBodyPrompt":
        prompt = BODY_TOYBOX_PROMT.format(
            box_color=box_color,
            in_box=in_box,
            box_name=box_name,
        )

        return cls(prompt=prompt)

    @classmethod
    def cosmetic(
        cls,
    ) -> "R2PBodyPrompt":
        return cls(
            prompt=BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT,
        )

    @classmethod
    def calories(
        cls,
        description: str | None = None,
    ) -> "R2PBodyPrompt":
        user_text = (
            f"Analyze this food: {description}"
            if description
            else "Analyze the food on uploaded image:"
        )
        full_prompt = f"{BODY_CALORIES_SYSTEM_PROMPT}\n\n{user_text}"
        return cls(prompt=full_prompt)

    @classmethod
    def instagram(
        cls,
        prompt: str,
    ) -> "R2PBodyPrompt":
        user_text = f"Use this description: {prompt}"
        full_prompt = f"{BODY_POST_CREATOR_SYSTEM_PROMPT}\n\n{user_text}"
        return cls(prompt=full_prompt)

    @classmethod
    def gamestone(
        cls,
    ) -> "R2PBodyPrompt":
        return cls(
            prompt=BODY_GEMSTONE_PROMPT,
        )

    @classmethod
    def day_fact(
        cls,
    ) -> "R2PBodyPrompt":
        return cls(
            prompt=BODY_FACT_DAY_PROMPT,
        )

    @classmethod
    def honestly(
        cls,
    ) -> "R2PBodyPrompt":
        return cls(
            prompt=BODY_HONESTLY_PROMPT,
        )

    @classmethod
    def face_swap(
        cls,
    ) -> "R2PBodyPrompt":
        return cls(
            prompt=BODY_FACE_SWAP_PROMPT,
        )


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
        str | None,
        Field(default=None),
    ]
    image_url: Annotated[
        str | None,
        Field(default=None),
    ]


class IMessage(ISchema):
    role: Annotated[
        str,
        Field(...),
    ]
    content: list[Union[str, ITextContent, IImageContent]]


class CaloriesBody(ISchema):
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
    def create_text(cls, description: str) -> "CaloriesBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_CALORIES_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[ITextContent(text=f"Analyze this food: {description}")],
                ),
            ],
        )

    @classmethod
    def create_image(cls, image_url: str) -> "CaloriesBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_CALORIES_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(text="Analyze the food in this image."),
                        IImageContent(image_url=IImageUrl(url=image_url)),
                    ],
                ),
            ],
        )


class CaloriesWeightBody(ISchema):
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
    def create_image(cls, image_url: str) -> "CaloriesBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=NUTRITION_ANALYSIS_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(text="Analyze the food in this image."),
                        IImageContent(image_url=IImageUrl(url=image_url)),
                    ],
                ),
            ],
        )

    @classmethod
    def create_text(cls, description: str) -> "CaloriesBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=NUTRITION_ANALYSIS_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[ITextContent(text=f"Analyze this food: {description}")],
                ),
            ],
        )


class CosmeticBody(ISchema):
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
    def create_text(cls, description: str) -> "CosmeticBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(
                            text=f"Analyze the following cosmetic products: {description}"
                        )
                    ],
                ),
            ],
        )

    @classmethod
    def create_image(cls, image_url: str) -> "CosmeticBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(
                            text="Please identify and list all visible cosmetic products in this photo. Include brand names, product types, and packaging characteristics if possible."
                        ),
                        IImageContent(image_url=IImageUrl(url=image_url)),
                    ],
                ),
            ],
        )


class FaceSwapBody(ISchema):
    model: Annotated[
        str,
        Field(default="gpt-4.1"),
    ]
    messages: list[IMessage]

    @classmethod
    def create_text(
        cls,
        text: str,
        image1: str,
        image2: str,
    ) -> "CosmeticBody":
        return cls(
            model="gpt-4.1",
            messages=[
                IMessage(
                    role="user",
                    content=[
                        ITextContent(text=text),
                        ITextContent(type="input_image", image_url=image1),
                        ITextContent(type="input_image", image_url=image2),
                    ],
                ),
            ],
        )

    @classmethod
    def create_image(cls, image_url: str) -> "CosmeticBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_COSMETIC_PRODUCT_SYSTEM_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(
                            text="Please identify and list all visible cosmetic products in this photo. Include brand names, product types, and packaging characteristics if possible."
                        ),
                        IImageContent(image_url=IImageUrl(url=image_url)),
                    ],
                ),
            ],
        )


class AntiquesBody(ISchema):
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
    def create_image(cls, image_url: str) -> "CaloriesBody":
        return cls(
            model="gpt-4o",
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                IMessage(
                    role="system",
                    content=[ITextContent(text=BODY_ANTIQUES_PROMPT)],
                ),
                IMessage(
                    role="user",
                    content=[
                        ITextContent(text="Analyze the antiques in this image."),
                        IImageContent(image_url=IImageUrl(url=image_url)),
                    ],
                ),
            ],
        )


class IFaceSwapData(ISchema):
    model: Annotated[
        str,
        Field(default="gpt-image-1"),
    ]
    prompt: Annotated[
        str,
        Field(...),
    ]
