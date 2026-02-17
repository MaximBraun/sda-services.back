# coding utf-8

from functools import cached_property

from celery import Celery

from ....entities.core import (
    IConfEnv,
)


class ICelery:
    def __init__(
        self,
        app_name: str,
        conf: IConfEnv,
    ) -> None:
        self._app_name = app_name
        self._conf = conf

    @cached_property
    def celery(
        self,
    ) -> Celery:
        return Celery(
            main=self._app_name,
            broker=self._conf.rabbitmq_dsn_url,
            # backend=self._conf.redis_dsn_url,
        )

    def register_tasks(self) -> None: ...
