# coding utf-8

from typing import Annotated, Any

from pydantic import Field

from datetime import datetime

from .base import ISchema


class AppWebhook(ISchema):
    bundle_id: Annotated[
        str,
        Field(...),
    ]


class EventProperties(ISchema):
    product_id: Annotated[
        str,
        Field(...),
    ]


class EventWebhook(ISchema):
    id: Annotated[
        str,
        Field(...),
    ]
    created_at: Annotated[
        str,
        Field(...),
    ]
    properties: Annotated[
        EventProperties,
        Field(...),
    ]
    name: Annotated[
        str,
        Field(...),
    ]


class UserWebhook(ISchema):
    created_at: Annotated[
        str,
        Field(...),
    ]
    user_id: Annotated[
        str,
        Field(...),
    ]
    total_spent: Annotated[
        float | int,
        Field(...),
    ]
    payments_count: Annotated[
        float | int,
        Field(...),
    ]


class IWebhook(ISchema):
    app: Annotated[
        AppWebhook,
        Field(...),
    ]
    event: Annotated[
        EventWebhook,
        Field(...),
    ]
    user: Annotated[
        UserWebhook,
        Field(...),
    ]
