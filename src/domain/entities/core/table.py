# coding utf-8

from re import sub

from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

from ...constants import (
    TABLE_PATTERN,
    TABLE_REPLACEMENT,
)


class ITable(DeclarativeBase):
    """
    Abstract base class for database table definitions.
    Provides automatic table name generation from class name following a standard pattern.
    """

    __name__: str

    @declared_attr.directive
    def __tablename__(
        cls,
    ) -> str:
        """
        Generates a standardized table name from the class name."
        """

        return sub(
            TABLE_PATTERN,
            TABLE_REPLACEMENT,
            cls.__name__,
        ).lower()
