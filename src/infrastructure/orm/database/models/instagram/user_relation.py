# coding utf-8

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
)

from sqlalchemy.orm import relationship

from ......domain.entities.core import ITable

from ......domain.typing.enums import InstagramRelationType


class InstagramUserRelations(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
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
    relation_type: str = Column(
        String,
        nullable=False,
    )
    related_username: str = Column(
        String(128),
        nullable=False,
    )
    related_full_name: str = Column(
        String(128),
        nullable=True,
    )
    related_user_id: str = Column(
        String(64),
        nullable=True,
    )
    profile_picture: str = Column(
        String(1024),
        nullable=False,
    )
    created_at: str = Column(
        DateTime,
        nullable=False,
    )
