# coding utf-8

from fastapi import Request

from os import getenv

from fastapi.responses import JSONResponse

from fastapi.exceptions import HTTPException

from ...domain.conf import app_conf

from ...domain.constants import ERROR_TRANSLATIONS

from ...domain.tools import format_error_with_request

from ...domain.entities.core import IConfEnv

from ...domain.entities.bot import IBotReporter


conf: IConfEnv = app_conf()


telegram_bot = IBotReporter(
    conf,
)


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    title = ERROR_TRANSLATIONS.get(
        exc.detail,
        "Произошла неизвестная ошибка",
    )
    project = getenv("APP_SERVICE", "Default")

    message = await format_error_with_request(
        exc=exc,
        status_code=exc.status_code,
        request=request,
        title=title,
        project=project,
    )

    await telegram_bot.send_error(text=message)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )
