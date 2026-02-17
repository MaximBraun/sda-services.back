# coding utf-8

from typing import Annotated, Optional, List

from pydantic import Field, field_validator

from fastapi import UploadFile

from base64 import b64encode

from ..core import ISchema


class XimilarAuthBody(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]


class XimilarAuthResponse(ISchema):
    access: Annotated[
        str,
        Field(...),
    ]
    refresh: Annotated[
        str,
        Field(...),
    ]


class XimilarImage(ISchema):
    base64: Annotated[
        str,
        Field(..., alias="_base64"),
    ]


class XimilarCardBody(ISchema):
    records: Annotated[
        list[XimilarImage],
        Field(...),
    ]
    pricing: Annotated[
        bool,
        Field(default=True),
    ]

    @classmethod
    async def from_upload(
        cls,
        image: UploadFile,
    ) -> "XimilarCardBody":
        image_bytes = await image.read()

        base64_str = b64encode(image_bytes).decode("utf-8")

        data_uri = f"data:{image.content_type};base64,{base64_str}"

        return cls(
            records=[XimilarImage(base64=data_uri)],
            pricing=True,
        )


class PriceInfo(ISchema):
    standart: Annotated[
        Optional[float] | str,
        Field(default=None),
    ]
    foil: Annotated[
        Optional[float] | str,
        Field(default=None),
    ]

    @field_validator("foil", mode="after")
    @classmethod
    def validate_foil(
        cls,
        value: float | None,
    ) -> str | None:
        if value is not None:
            return f"{value}$"
        return value

    @field_validator("standart", mode="after")
    @classmethod
    def validate_standart(
        cls,
        value: float | None,
    ) -> str | None:
        if value is not None:
            return f"{value}$"
        return value


class CardResponse(ISchema):
    image: Annotated[
        Optional[str],
        Field(default=None),
    ]
    full_name: Annotated[
        str,
        Field(...),
    ]
    rarity: Annotated[
        str,
        Field(...),
    ]
    version: Annotated[
        str,
        Field(...),
    ]
    number: Annotated[
        str,
        Field(...),
    ]
    set: Annotated[
        str,
        Field(...),
    ]
    price: Annotated[
        PriceInfo,
        Field(...),
    ]

    @classmethod
    def from_best_match(
        cls,
        best_match: dict,
    ) -> "CardResponse":
        pricing_list: List[dict] = best_match.get("pricing", {}).get("list", [])

        nonfoil_prices = [
            p["price"] for p in pricing_list if p.get("version") == "Non-Foil"
        ]
        foil_prices = [p["price"] for p in pricing_list if p.get("version") == "Foil"]

        price_data = PriceInfo(
            standart=max(nonfoil_prices) if nonfoil_prices else None,
            foil=max(foil_prices) if foil_prices else None,
        )

        image_url = pricing_list[0].get("img_link") if pricing_list else None

        return cls(
            image=image_url,
            full_name=best_match.get("full_name", ""),
            rarity=best_match.get("rarity", ""),
            number=best_match.get("card_number", ""),
            version=best_match.get("title", ""),
            set=best_match.get("set", ""),
            price=price_data,
        )

    @classmethod
    def from_full_response(
        cls,
        data: dict,
    ) -> "CardResponse":
        records = data.get("records", [])
        if not records:
            raise ValueError("records invalid")

        first = records[0]

        objects = first.get("_objects", [])
        if not objects:
            raise ValueError("_objects invalid")

        identified_obj = next(
            (obj for obj in objects if "_identification" in obj), None
        )

        if not identified_obj:
            raise ValueError("There'ant objects with _identification")

        best_match = identified_obj["_identification"].get("best_match")
        if not best_match:
            raise ValueError("Best_match not in _identification")

        return cls.from_best_match(best_match)
