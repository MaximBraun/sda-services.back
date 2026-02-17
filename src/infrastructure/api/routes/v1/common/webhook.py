# coding utf-8

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Depends,
)

from ......domain.tools import (
    add_user_tokens,
    fetch_webhook_id,
)

from ......domain.entities.core import IWebhook


webhook_router = APIRouter(
    tags=["Webhooks"],
)


@webhook_router.post(
    "/webhooks/{webhook_id}",
    status_code=200,
)
async def apphud_webhook(
    request: Request,
    webhook_id: str,
    valid_webhook_id: str = Depends(fetch_webhook_id),
) -> IWebhook:
    if request is None:
        raise HTTPException(
            status_code=400,
            detail="Error handling webhook.",
        )

    valid_webhook_id == webhook_id

    payload = await request.json()

    data = IWebhook(**payload)

    if data.event.name in (
        "subscription_started",
        "subscription_renewed",
        "non_renewing_purchase",
    ):
        await add_user_tokens(data)

    return data
