# coding utf-8

from ......domain.conf import app_conf

from ......domain.entities.core import IConfEnv

from ......domain.repositories import IDatabase

from ......infrastructure.orm.database.repositories import (
    PikaApplicationRepository,
    PikaTemplateRepository,
)


from .....schemas.api import (
    Application,
)


conf: IConfEnv = app_conf()


template_database = PikaTemplateRepository(
    IDatabase(conf),
)


class PikaApplicationController:
    def __init__(
        self,
        repository: PikaApplicationRepository,
    ) -> None:
        self._repository = repository

    async def fetch_applications(
        self,
        token_data: dict[str, int | str],
    ) -> list[Application]:
        return await self._repository.fetch_one_to_many(
            "auth_user_id",
            token_data.get("aid"),
            related=["templates"],
        )

    async def fetch_application_by_app_id(
        self,
        app_id: str,
    ) -> Application | None:
        return await self._repository.fetch_application(
            "app_id",
            app_id,
            ["templates"],
        )
