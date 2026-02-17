# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.dialects.mssql import TINYINT

from ......domain.entities.core import ITable


class QwenAccounts(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    username: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    password: str = Column(
        String,
        nullable=False,
    )
    is_active: bool = Column(
        TINYINT,
        default=1,
    )
    usage_count: int = Column(
        Integer,
        default=0,
        nullable=False,
    )
    user_id: str = Column(
        String,
        nullable=True,
    )
    auth_user_id: int = Column(
        Integer,
        nullable=False,
    )
