# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ......domain.tools import validate_token

from ......domain.entities.auth import IToken

user_router = APIRouter(tags=["User"])


@user_router.get(
    "/info",
    response_model=IToken,
)
async def fetch_user_info(
    token_data: dict[str, str | int] = Depends(validate_token),
) -> IToken:
    return IToken(
        **token_data,
    )
