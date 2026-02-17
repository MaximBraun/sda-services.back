# coding utf-8

from ......domain.conf import app_conf

from ......domain.entities.core import IConfEnv

from ......domain.repositories import IDatabase

from ......infrastructure.orm.database.repositories import (
    PixverseApplicationRepository,
    PixverseTemplateRepository,
)

from ......infrastructure.orm.database.models import (
    PixverseApplicationTemplates,
    PixverseApplicationStyles,
)

from .....schemas.api import (
    Application,
    PixverseApplication,
    ChangeApplication,
    AddPixverseApplication,
)


conf: IConfEnv = app_conf()


template_database = PixverseTemplateRepository(
    IDatabase(conf),
)


class PixverseApplicationController:
    def __init__(
        self,
        repository: PixverseApplicationRepository,
    ) -> None:
        self._repository = repository

    async def fetch_applications(
        self,
        token_data: dict[str, int | str],
    ) -> list[Application]:
        return await self._repository.fetch_one_to_many(
            "auth_user_id",
            token_data.get("aid"),
            related=["templates", "styles", "categories"],
        )

    async def fetch_application_by_app_id(
        self,
        app_id: str,
    ) -> Application | None:
        application = await self._repository.fetch_application(
            "app_id",
            app_id,
            ["templates", "styles", "categories"],
        )

        if application.categories is not None:
            categories = [category.title for category in application.categories]

            category_priority = {name: i for i, name in enumerate(categories)}

            if application.templates:
                application.templates.sort(
                    key=lambda t: category_priority.get(t.category, len(categories))
                )

        return application

    async def add_application(
        self,
        data: PixverseApplication,
        token_data: dict[str, int | str],
    ) -> PixverseApplication:
        return await self._repository.add_record(
            AddPixverseApplication(
                **data.dict,
                auth_user_id=token_data.get("aid"),
            ),
        )

    async def update_application(
        self,
        id: int,
        data: ChangeApplication,
        token_data: dict[str, int | str],
    ) -> PixverseApplication:
        application = await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )
        if application is not None:
            await self._repository.update_application(
                application_id=id,
                relation_table=PixverseApplicationTemplates,
                relation_ids=data.template_ids,
                relation_column_name="template_id",
            )

            await self._repository.update_application(
                application_id=id,
                relation_table=PixverseApplicationStyles,
                relation_ids=data.style_ids,
                relation_column_name="style_id",
            )

        return data

    async def delete_application(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> bool:
        application = await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )
        if application is not None:
            return await self._repository.delete_record(
                id,
            )
