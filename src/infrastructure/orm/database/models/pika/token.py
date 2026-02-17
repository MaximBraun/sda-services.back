# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from ......domain.entities.core import ITable


class PikaAccountsTokens(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    jwt_token: str = Column(
        String,
        nullable=False,
    )
    api_key: str = Column(
        String,
        nullable=False,
    )
    user_id: str = Column(
        String,
        nullable=False,
    )
    cookies: str = Column(
        String,
        nullable=False,
    )
    account_id: int = Column(
        Integer,
        nullable=False,
    )
