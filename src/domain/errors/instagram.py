# coding utf-8

from typing import ClassVar, Type

from ..entities.core import IError

from ..constants import INSTAGRAM_ERROR


class InstagramError(IError):
    exceptions: ClassVar[tuple[Type[Exception], ...]] = tuple(INSTAGRAM_ERROR.keys())

    def __init__(
        self,
        status_code: int,
        detail: str,
        extra: dict[str] = {},
    ) -> None:
        self.extra = extra
        super().__init__(
            status_code=status_code,
            detail=detail,
        )

    @classmethod
    def from_exception(
        cls,
        exc: Exception,
    ) -> "InstagramError":
        exc_type = exc if isinstance(exc, type) else type(exc)
        status_code, detail = INSTAGRAM_ERROR.get(exc_type, (400, str(exc)))
        return cls(
            status_code=status_code,
            detail=detail,
        )
