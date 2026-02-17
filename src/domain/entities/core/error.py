# coding utf-8

from fastapi import HTTPException


class IError(HTTPException):
    """
    Кастомное исключение HTTP с возможностью задавать статус и сообщение.

    Args:
        status_code (int): HTTP статус код ошибки.
        detail (str): Детальное описание ошибки.
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            status_code,
            detail,
        )
