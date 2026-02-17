# coding utf-8

from ..entities.core import IError

from ..constants import TOPMEDIA_ERROR


class TopmediaError(IError):
    """
    Исключение, возникающее при неверных учетных данных.

    Args:
        status_code (int, optional): HTTP статус код ошибки. По умолчанию `ErrorCode.unauthorized`.
        detail (str, optional): Сообщение об ошибке. По умолчанию "Invalid credentials provided".
    """

    def __init__(
        self,
        status_code: int,
        extra: dict[str] = {},
    ) -> None:
        self.extra = extra
        args = dict(
            zip(
                ("status_code", "detail"),
                TOPMEDIA_ERROR.get(
                    status_code,
                    TOPMEDIA_ERROR[500],
                ),
            )
        )
        super().__init__(**args)
