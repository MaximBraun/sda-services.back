# coding utf-8

from ..conf import app_conf

from fastapi import HTTPException, Depends

from ..entities.core import IConfEnv

from ..repositories import IDatabase

from ...infrastructure.orm.database.repositories import WebhookRepository

conf: IConfEnv = app_conf()


webhook_repository = WebhookRepository(
    IDatabase(conf),
)


async def fetch_webhook_id(
    webhook_id: str,
) -> bool:
    webhook_data = await webhook_repository.fetch_with_filters(
        uuid=webhook_id,
    )
    if webhook_data is not None:
        return True
    raise HTTPException(status_code=404, detail="Webhook not found")
