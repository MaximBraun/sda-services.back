# coding utf-8

from uuid import uuid4

from sqlalchemy import (
    Column,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from sqlalchemy.dialects.mysql import TINYINT

from ..common import UserServices

from ......domain.entities.core import ITable


class AuthUsers(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        unique=True,
    )
    uuid: str = Column(
        String,
        default=uuid4(),
        nullable=False,
        primary_key=True,
    )
    username: str = Column(
        String(length=150),
        nullable=False,
        primary_key=True,
    )
    email: str = Column(
        String(length=254),
        nullable=False,
        primary_key=True,
    )
    role: str = Column(
        String(length=32),
        nullable=False,
        default="user",
    )
    is_active: int = Column(
        TINYINT,
        default=1,
        nullable=False,
    )
    password: str = Column(
        String(length=128),
        nullable=False,
    )

    services = relationship(
        "Services",
        secondary=UserServices,
        back_populates="user",
    )
