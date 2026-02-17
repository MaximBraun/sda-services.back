# coding utf-8

from functools import cached_property

from ....domain.conf import app_conf

from ....domain.entities.core import IConfEnv

from ....domain.repositories import (
    ICelery,
)

from ....infrastructure.external.pika import (
    PikaClient,
    PikaSessionCore,
    PikaCore,
)


class PikaCelery(ICelery):
    def __init__(
        self,
        app_name: str = "pika",
        conf: IConfEnv = app_conf(),
    ) -> None:
        super().__init__(
            app_name,
            conf,
        )

    @cached_property
    def client(
        self,
    ) -> PikaClient:
        return PikaClient(
            core=PikaCore(),
            session=PikaSessionCore(),
        )
