# coding utf-8

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from sqlalchemy.orm import relationship

from ......domain.entities.core import ITable


class InstagramUsers(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    username: str = Column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )
    full_name: str = Column(
        String(64),
        nullable=False,
    )
    biography: str = Column(
        String(256),
        nullable=True,
    )
    profile_picture: str = Column(
        String(512),
        nullable=True,
    )
    is_private: bool = Column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_verified: bool = Column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_business_account: bool = Column(
        Boolean,
        default=False,
        nullable=False,
    )
    user_id: int = Column(
        Integer,
        unique=True,
        index=True,
    )

    statistics = relationship(
        "InstagramUserStats",
        back_populates="user",
    )

    publications = relationship(
        "InstagramUserPosts",
        back_populates="user",
    )

    tracking_users = relationship(
        "InstagramTracking",
        foreign_keys="InstagramTracking.target_user_id",
        back_populates="target_user_data",
    )
