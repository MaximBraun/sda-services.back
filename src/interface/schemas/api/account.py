# coding utf-8

from typing import Annotated

from pydantic import Field

from ....domain.entities.core import ISchema


class IAccount(ISchema):
    username: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]


class AddAccount(IAccount):
    user_id: Annotated[
        int,
        Field(..., alias="auth_user_id"),
    ]


class ChangeAccount(IAccount):
    is_active: Annotated[
        bool,
        Field(default=0),
    ]
    balance: Annotated[
        int,
        Field(default=0),
    ]


class Account(ChangeAccount):
    id: Annotated[
        int,
        Field(...),
    ]


class AccountBalance(ISchema):
    balance: Annotated[
        int,
        Field(...),
    ]
    is_active: Annotated[
        bool,
        Field(default=1),
    ]
