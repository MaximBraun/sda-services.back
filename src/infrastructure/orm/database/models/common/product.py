# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
)

from sqlalchemy.orm import relationship

from .one_to_many import ApplicationProducts

from ......domain.entities.core import ITable


class Products(ITable):
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: str = Column(
        String(128),
        nullable=False,
    )
    tokens_amount: int = Column(
        Integer,
        default=0,
        nullable=True,
    )
    is_active: bool = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    applications = relationship(
        "Applications",
        secondary=ApplicationProducts,
        back_populates="products",
    )
