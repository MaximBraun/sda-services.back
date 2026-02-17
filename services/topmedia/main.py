# coding utf-8

from fastapi import FastAPI, HTTPException

from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from src.domain.conf import app_conf

from src.domain.entities.core import IConfEnv

from src.interface.server.components import TopmediaRouter

from src.interface.middleware import LimitUploadSize

from src.interface.handlers import http_exception_handler


def main() -> FastAPI:
    conf: IConfEnv = app_conf()

    app = FastAPI(**conf.app_config)

    app_router = TopmediaRouter(app, conf)

    app.mount(
        "/static",
        StaticFiles(directory="uploads"),
        name="static",
    )

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_middleware(LimitUploadSize)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
    )
    app_router.create()

    return app


if __name__ == "__main__":
    main()
