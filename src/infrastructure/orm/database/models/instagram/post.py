# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Float,
)

from sqlalchemy.orm import relationship

from datetime import datetime

from ......domain.entities.core import ITable


class InstagramUserPosts(ITable):
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
    )

    likes_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )

    comments_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )

    views_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )

    avg_likes: float = Column(
        Float,
        default=0.0,
        nullable=True,
    )

    avg_views: float = Column(
        Float,
        default=0.0,
        nullable=True,
    )

    post_url: str = Column(
        String(length=256),
        nullable=False,
    )

    thumbnail_url: str = Column(
        String(length=256),
        nullable=True,
    )

    created_at: datetime = Column(
        DateTime,
        nullable=False,
    )

    user = relationship(
        "InstagramUsers",
        back_populates="publications",
    )
