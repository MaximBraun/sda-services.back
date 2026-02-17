# coding utf-8

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import relationship

from datetime import datetime

from ......domain.entities.core import ITable


class InstagramUserStats(ITable):
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
    tracking_id: int = Column(
        Integer,
        ForeignKey(
            "instagram_tracking.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        index=True,
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
    publications_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )
    followers_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )
    following_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )
    mutual_subscriptions_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )
    non_reciprocal_following_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )
    non_reciprocal_followers_count: int = Column(
        Integer,
        default=0,
        nullable=True,
    )
    created_at: datetime = Column(
        DateTime,
        nullable=False,
        default=datetime,
    )

    user = relationship(
        "InstagramUsers",
        back_populates="statistics",
    )

    tracking = relationship(
        "InstagramTracking",
        back_populates="statistics",
    )
