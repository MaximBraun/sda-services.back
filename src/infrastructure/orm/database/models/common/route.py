# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from .one_to_many import ServiceRoutes

from ......domain.entities.core import ITable


class Routes(ITable):
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: str = Column(
        String(64),
        nullable=False,
    )

    service = relationship(
        "Services",
        secondary=ServiceRoutes,
        back_populates="routes",
    )
