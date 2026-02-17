# coding utf-8

from ......domain.conf import app_conf

from ......domain.entities.core import IConfEnv

from ......domain.repositories import IDatabase

from ......infrastructure.orm.database.repositories import (
    PhotoGeneratorApplicationRepository,
    PhotoGeneratorTemplateRepository,
)

from ......infrastructure.orm.database.models import (
    PhotoGeneratorApplicationTemplates,
)

from .....schemas.api import (
    Application,
    PhotoGeneratorApplication,
    ChangeApplication,
)


conf: IConfEnv = app_conf()


template_database = PhotoGeneratorTemplateRepository(
    IDatabase(conf),
)


class PhotoGeneratorApplicationController:
    def __init__(
        self,
        repository: PhotoGeneratorApplicationRepository,
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

    async def add_application(
        self,
        data: PhotoGeneratorApplication,
    ) -> PhotoGeneratorApplication:
        return await self._repository.add_record(
            data,
        )

    async def update_application(
        self,
        id: int,
        data: ChangeApplication,
    ) -> PhotoGeneratorApplication:
        await self._repository.update_application(
            application_id=id,
            relation_table=PhotoGeneratorApplicationTemplates,
            relation_ids=data.template_ids,
            relation_column_name="template_id",
        )

        return data

    async def delete_application(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )
