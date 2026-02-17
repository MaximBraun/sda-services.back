# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
)

from sqlalchemy.orm import relationship

from datetime import datetime

from .one_to_many import ApplicationProducts

from ......domain.entities.core import ITable


class Applications(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    name: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    application_id: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    description: str = Column(
        String,
        nullable=True,
    )
    region: str = Column(
        String,
        nullable=True,
    )
    store_region: str = Column(
        String,
        nullable=True,
    )
    application_number: str = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )
    category: str = Column(
        String,
        nullable=True,
    )
    start_date: datetime = Column(
        DateTime,
        nullable=True,
    )
    release_date: datetime = Column(
        DateTime,
        nullable=True,
    )
    technology: str = Column(
        String,
        nullable=True,
    )
    webhook_url: str = Column(
        String,
        nullable=True,
    )
    auth_user_id: int = Column(
        Integer,
        nullable=False,
    )
    available_tokens: bool = Column(
        Boolean,
        nullable=False,
    )

    products = relationship(
        "Products",
        secondary=ApplicationProducts,
        back_populates="applications",
    )
