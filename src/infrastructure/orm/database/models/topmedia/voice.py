# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
)

from ......domain.entities.core import ITable


class TopmediaVoices(ITable):
    id: int = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=1,
    )
    name: str = Column(
        String,
        nullable=False,
        unique=True,
    )
    is_active: bool = Column(
        Boolean,
        nullable=False,
    )
    speaker: str = Column(
        String,
        nullable=False,
    )
    avatar_url: str = Column(
        String,
        nullable=False,
    )
    avatar_url_webp: str = Column(
        String,
        nullable=False,
    )
    audition_url: str = Column(
        String,
        nullable=False,
    )
