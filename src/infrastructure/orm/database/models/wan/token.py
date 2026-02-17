# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from ......domain.entities.core import ITable


class WanAccountsTokens(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    cookies: str = Column(
        String,
        nullable=False,
    )
    account_id: int = Column(
        Integer,
        nullable=False,
    )
