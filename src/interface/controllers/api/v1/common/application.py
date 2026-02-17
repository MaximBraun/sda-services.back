# coding utf-8

from ......infrastructure.orm.database.repositories import (
    ApplicationRepository,
    WebhookRepository,
)

from ......interface.schemas.api import (
    StoreApplication,
    ChangeStoreApplication,
    AddStoreApplication,
    IAddStoreApplication,
    Webhook,
)

from ......domain.entities.core import IConfEnv

from ......domain.repositories.engines import IDatabase

from ......domain.conf import app_conf


conf: IConfEnv = app_conf()


webhook_repository = WebhookRepository(
    IDatabase(
        conf,
    )
)


class ApplicationController:
    def __init__(
        self,
        repository: ApplicationRepository,
    ) -> None:
        self._repository = repository

    async def fetch_applications(
        self,
        token_data: dict[str, int | str],
    ) -> list[StoreApplication]:
        return await self._repository.fetch_one_to_many(
            "auth_user_id",
            token_data.get("aid"),
            related=["products"],
        )

    async def fetch_application(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> StoreApplication:
        return await self._repository.fetch_with_filters(
            id=id,
            auth_user_id=token_data.get("aid"),
        )

    async def add_application(
        self,
        data: AddStoreApplication,
        token_data: dict[str, int | str],
    ) -> AddStoreApplication:
        webhooks = await webhook_repository.fetch_all()

        valid_app_ids = {webhook.app_id for webhook in webhooks}
        if data.application_id not in valid_app_ids:
            await webhook_repository.add_record(
                Webhook(app_id=data.application_id),
            )

        fetched_webhook = await webhook_repository.fetch_with_filters(
            app_id=data.application_id
        )

        return await self._repository.add_record(
            IAddStoreApplication(
                **data.dict,
                webhook_url=fetched_webhook.uuid,
                auth_user_id=token_data.get("aid"),
            )
        )

    async def delete_application(
        self,
        id: int,
        token_data: dict[str, int | str],
    ) -> bool:
        application = await self._repository.fetch_with_filters(
            auth_user_id=token_data.get("aid")
        )
        if application is not None:
            return await self._repository.delete_record(
                id,
            )
        return False

    async def update_application(
        self,
        id: int,
        data: ChangeStoreApplication,
        token_data: dict[str, int | str],
    ) -> ChangeStoreApplication:
        application = await self._repository.fetch_with_filters(
            auth_user_id=token_data.get("aid")
        )
        if application is not None:
            return await self._repository.update_record(
                id,
                data,
            )
