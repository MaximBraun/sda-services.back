# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from .one_to_many import (
    UserServices,
    ServiceRoutes,
)

from ......domain.entities.core import ITable


class Services(ITable):
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: str = Column(
        String(128),
        nullable=False,
    )

    user = relationship(
        "AuthUsers",
        secondary=UserServices,
        back_populates="services",
    )

    routes = relationship(
        "Routes",
        secondary=ServiceRoutes,
        lazy="joined",
        back_populates="service",
    )
