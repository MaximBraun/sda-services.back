# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from ..common import (
    WanApplicationTemplates,
    WanAccountApplications,
)

from ......domain.entities.core import ITable


class WanApplications(ITable):
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
        "WanTemplates",
        secondary=WanApplicationTemplates,
        back_populates="applications",
    )

    accounts = relationship(
        "WanAccounts",
        WanAccountApplications,
        back_populates="applications",
    )
