# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from ..common import PixverseApplicationCatagories

from ......domain.entities.core import ITable


class PixverseCategories(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    title: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )

    applications = relationship(
        "PixverseApplications",
        secondary=PixverseApplicationCatagories,
        back_populates="categories",
    )
