# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from ..common import XimilarAccountApplications

from ......domain.entities.core import ITable


class XimilarApplications(ITable):
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

    accounts = relationship(
        "XimilarAccounts",
        XimilarAccountApplications,
        back_populates="applications",
    )
