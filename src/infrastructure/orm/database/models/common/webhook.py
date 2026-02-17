# coding utf-8

from sqlalchemy import (
    Column,
    String,
)

from ......domain.entities.core import ITable


class Webhooks(ITable):
    uuid: int = Column(
        String,
        nullable=False,
        primary_key=True,
    )
    app_id: str = Column(
        String,
        nullable=False,
    )
