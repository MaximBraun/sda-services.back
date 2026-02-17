# coding utf-8

from ..entities.core import IError

from ..constants import WAN_ERROR


class WanError(IError):
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
                WAN_ERROR.get(
                    status_code,
                    WAN_ERROR[9999],
                ),
            )
        )
        super().__init__(**args)
