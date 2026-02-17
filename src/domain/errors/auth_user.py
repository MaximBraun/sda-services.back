# coding utf-8

from ..entities.core import IError

from ..typing.enums import RequestError


class TokenError(IError):
    def __init__(
        self,
        status_code=RequestError.FORBIDDEN,
        detail: str = "Invalid Token provided",
        headers: dict = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )


class CredentialsError(IError):
    def __init__(
        self,
        status_code=RequestError.FORBIDDEN,
        detail: str = "Invalid user's credentials provided",
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
        )
