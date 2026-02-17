# coding utf-8

from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
)

from datetime import datetime

from ......domain.entities.core import ITable


class InstagramSessions(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    uuid: str = Column(
        String(length=36),
        default=str(uuid4()),
        nullable=False,
        index=True,
        unique=True,
    )
    csrftoken: str = Column(
        String(length=64),
        nullable=False,
    )
    ds_user_id: str = Column(
        String(length=32),
        nullable=False,
    )
    sessionid: str = Column(
        String(length=128),
        nullable=False,
    )
    user_id: int = Column(
        Integer,
        ForeignKey(
            "instagram_users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    created_at: datetime = Column(
        DateTime,
        nullable=False,
    )
