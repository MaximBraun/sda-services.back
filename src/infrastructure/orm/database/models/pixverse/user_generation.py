# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)

from datetime import datetime

from ......domain.entities.core import ITable


class UserGenerations(ITable):
    uuid: int = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    generation_id: int = Column(
        Integer,
        nullable=True,
        unique=True,
    )
    account_id: int = Column(
        Integer,
        nullable=False,
    )
    user_id: str = Column(
        Integer,
        nullable=False,
    )
    app_id: str = Column(
        Integer,
        nullable=False,
    )
    app_name: str = Column(
        String,
        nullable=False,
    )
    generation_url: str = Column(
        String,
        nullable=True,
    )
    created_at: datetime = Column(
        DateTime,
        nullable=True,
    )
