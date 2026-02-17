# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
)

from sqlalchemy.orm import relationship

from ..common import PixverseApplicationStyles

from ......domain.entities.core import ITable


class PixverseStyles(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    template_id: int = Column(
        Integer,
        nullable=True,
        primary_key=True,
    )
    prompt: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    name: str = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    preview_small: str = Column(
        String,
        nullable=False,
    )
    preview_large: str = Column(
        String,
        nullable=False,
    )
    is_active: bool = Column(
        Boolean,
        nullable=False,
        default=1,
    )
    auth_user_id: int = Column(
        Integer,
        nullable=False,
    )

    applications = relationship(
        "PixverseApplications",
        secondary=PixverseApplicationStyles,
        back_populates="styles",
    )
