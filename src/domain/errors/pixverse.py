# coding utf-8

from ..entities.core import IError

from ..constants import PIXVERSE_ERROR


class PixverseError(IError):
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
                PIXVERSE_ERROR.get(
                    status_code,
                    PIXVERSE_ERROR[99999],
                ),
            )
        )
        super().__init__(**args)
