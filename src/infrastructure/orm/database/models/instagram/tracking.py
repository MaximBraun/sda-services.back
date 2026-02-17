# coding utf-8

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from datetime import datetime

from sqlalchemy.orm import relationship

from ......domain.entities.core import ITable


class InstagramTracking(ITable):
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    target_user_id: int = Column(
        Integer,
        ForeignKey(
            "instagram_users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    owner_user_id: int = Column(
        Integer,
        ForeignKey(
            "instagram_users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    created_at: datetime = Column(
        DateTime,
        nullable=False,
        default=datetime,
    )

    target_user_data = relationship(
        "InstagramUsers",
        foreign_keys=[target_user_id],
        back_populates="tracking_users",
    )

    statistics = relationship(
        "InstagramUserStats",
        back_populates="tracking",
    )
