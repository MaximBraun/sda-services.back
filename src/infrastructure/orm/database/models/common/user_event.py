# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)

from datetime import datetime

from ......domain.entities.core import ITable


class UserEvents(ITable):
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: str = Column(
        String(128),
        nullable=False,
    )
    user_id: str = Column(
        String(256),
        nullable=False,
    )
    bundle_id: str = Column(
        String(128),
        nullable=False,
    )
    product_id: str = Column(
        String(128),
        nullable=False,
    )
    created_at: datetime = Column(
        DateTime,
        nullable=False,
    )
