# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import relationship

from ..common import XimilarAccountApplications

from sqlalchemy.dialects.mssql import TINYINT

from ......domain.entities.core import ITable


class XimilarAccounts(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    username: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    password: str = Column(
        String,
        nullable=False,
    )
    balance: int = Column(
        Integer,
        default=0,
        nullable=False,
    )
    is_active: bool = Column(
        TINYINT,
        default=1,
    )
    usage_count: int = Column(
        Integer,
        default=0,
        nullable=False,
    )
    auth_user_id: int = Column(
        Integer,
        nullable=False,
    )

    applications = relationship(
        "XimilarApplications",
        XimilarAccountApplications,
        back_populates="accounts",
    )
