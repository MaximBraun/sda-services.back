# coding utf-8

from ..entities.core import IError


class CaloriesError(IError):
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
