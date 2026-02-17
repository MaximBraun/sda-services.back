# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from ..common import (
    PhotoGeneratorApplicationTemplates,
)

from ......domain.entities.core import ITable


class PhotoGeneratorApplications(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    app_id: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    auth_user_id: int = Column(
        Integer,
        nullable=False,
    )

    templates = relationship(
        "PhotoGeneratorTemplates",
        secondary=PhotoGeneratorApplicationTemplates,
        back_populates="applications",
    )
