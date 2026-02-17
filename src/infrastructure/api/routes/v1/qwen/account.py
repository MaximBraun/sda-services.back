# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import QwenAccountView

from ......domain.tools import (
    auto_docs,
    validate_token,
)

from .....factroies.api.v1 import QwenAccountViewFactory

from ......interface.schemas.api.account import (
    Account,
    IAccount,
    ChangeAccount,
)


qwen_account_router = APIRouter(tags=["Accounts"])


@qwen_account_router.get(
    "/accounts",
    include_in_schema=False,
)
async def fetch_accounts(
    token_data: dict[str, str | int] = Depends(validate_token),
    view: QwenAccountView = Depends(QwenAccountViewFactory.create),
) -> list[Account]:
    return await view.fetch_accounts(
        token_data,
    )


@qwen_account_router.get(
    "/accounts/{id}",
    include_in_schema=False,
)
async def fetch_account(
    id: int,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: QwenAccountView = Depends(QwenAccountViewFactory.create),
) -> Account:
    return await view.fetch_account(
        id,
        token_data,
    )


@qwen_account_router.post(
    "/accounts",
    include_in_schema=False,
)
async def add_account(
    data: IAccount,
    token_data: dict[str, str | int] = Depends(validate_token),
    view: QwenAccountView = Depends(QwenAccountViewFactory.create),
) -> ChangeAccount:
    return await view.add_account(
        data,
        token_data,
    )


@qwen_account_router.put(
    "/accounts/{id}",
    include_in_schema=False,
)
async def update_account(
    id: int,
    data: ChangeAccount,
    token_data: dict[str, int | str] = Depends(validate_token),
    view: QwenAccountView = Depends(QwenAccountViewFactory.create),
) -> ChangeAccount:
    return await view.update_account(
        id,
        data,
        token_data,
    )


@qwen_account_router.delete(
    "/accounts/{id}",
    include_in_schema=False,
)
async def delete_account(
    id: int,
    token_data: dict[str, int | str] = Depends(validate_token),
    view: QwenAccountView = Depends(QwenAccountViewFactory.create),
) -> bool:
    return await view.delete_account(
        id,
        token_data,
    )
