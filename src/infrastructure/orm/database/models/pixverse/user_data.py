# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)

from datetime import datetime

from ......domain.entities.core import ITable


class UserData(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    user_id: int = Column(
        String,
        nullable=False,
    )
    app_id: str = Column(
        String,
        nullable=False,
    )
    balance: str = Column(
        Integer,
        default=0,
        nullable=False,
    )
    app_id_usage: str = Column(
        Integer,
        default=0,
        nullable=False,
    )
    created_at: datetime = Column(
        DateTime,
        nullable=True,
    )
