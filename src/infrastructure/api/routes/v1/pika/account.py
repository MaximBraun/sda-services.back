# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import PikaAccountView

from ......domain.tools import (
    validate_token,
)

from .....factroies.api.v1 import PikaAccountViewFactory

from ......interface.schemas.api.account import (
    Account,
)


pika_account_router = APIRouter(tags=["Accounts"])


@pika_account_router.get(
    "/accounts",
    include_in_schema=False,
)
async def fetch_accounts(
    token_data: dict[str, str | int] = Depends(validate_token),
    view: PikaAccountView = Depends(PikaAccountViewFactory.create),
) -> list[Account]:
    return await view.fetch_accounts(
        token_data,
    )
