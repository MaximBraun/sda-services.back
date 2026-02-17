# coding utf-8

from typing import Annotated

from pydantic import Field, field_validator

from datetime import datetime

from .template import Template

from .style import Style

from .product import Product

from .category import Category

from ....domain.entities.core import ISchema, IConfEnv

from ....domain.conf import app_conf


conf: IConfEnv = app_conf()


class IApplication(ISchema):
    app_id: Annotated[
        str,
        Field(...),
    ]
    templates: Annotated[
        list[Template] | None,
        Field(default=None),
    ]

    @field_validator("app_id", mode="before")
    @classmethod
    def validate_app_id(
        cls,
        value: str,
    ) -> str:
        return " ".join(value.split())


class PhotoGeneratorApplication(IApplication):
    pass


class PixverseApplication(IApplication):
    styles: Annotated[
        list[Style] | None,
        Field(default=None),
    ]


class AddPixverseApplication(IApplication):
    styles: Annotated[
        list[Style] | None,
        Field(default=None),
    ]
    auth_user_id: Annotated[
        int,
        Field(...),
    ]


class ChangeApplication(ISchema):
    app_id: Annotated[
        str,
        Field(...),
    ]
    template_ids: Annotated[
        list[int],
        Field(...),
    ]
    style_ids: Annotated[
        list[int],
        Field(...),
    ]


class Application(PixverseApplication):
    id: Annotated[
        int,
        Field(...),
    ]


class IStoreApplication(ISchema):
    name: Annotated[
        str,
        Field(...),
    ]
    region: Annotated[
        str,
        Field(...),
    ]
    application_number: Annotated[
        int,
        Field(...),
    ]
    technology: Annotated[
        str,
        Field(...),
    ]
    store_region: Annotated[
        str,
        Field(...),
    ]
    application_id: Annotated[
        str,
        Field(...),
    ]
    description: Annotated[
        str,
        Field(...),
    ]
    category: Annotated[
        str,
        Field(...),
    ]
    products: Annotated[
        list[Product] | None,
        Field(default=None),
    ]
    webhook_url: Annotated[
        str | None,
        Field(default=None),
    ]


class ChangeStoreApplication(IStoreApplication):
    pass


class AddStoreApplication(IStoreApplication):
    start_date: Annotated[
        datetime,
        Field(...),
    ]
    release_date: Annotated[
        datetime,
        Field(...),
    ]


class IAddStoreApplication(IStoreApplication):
    start_date: Annotated[
        datetime,
        Field(...),
    ]
    release_date: Annotated[
        datetime,
        Field(...),
    ]
    auth_user_id: Annotated[
        int,
        Field(...),
    ]


class StoreApplication(AddStoreApplication):
    id: Annotated[
        int,
        Field(...),
    ]

    @field_validator("webhook_url", mode="after")
    @classmethod
    def validate_webhook_url(
        cls,
        value: str,
    ):
        return f"{conf.domain_url}/pixverse/api/v1/webhooks/{value}"
