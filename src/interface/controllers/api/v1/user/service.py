# coding utf-8

from fastapi_pagination import (
    Page,
    paginate,
)

from ......infrastructure.orm.database.models import AuthUsers

from ......infrastructure.orm.database.repositories import AuthUserRepository

from .....schemas.api import (
    UserService,
)


class UserServiceController:
    def __init__(
        self,
        repository: AuthUserRepository,
    ) -> None:
        self._repository = repository

    async def fetch_services(
        self,
        token_data: dict[str, str | int],
    ) -> Page[UserService]:
        user: AuthUsers = await self._repository.fetch_one_to_many(
            "uuid",
            token_data.get("sub"),
            related=["services"],
            many=False,
        )

        items: list[UserService] = list(
            map(
                lambda service: UserService.model_validate(service),
                user.services,
            )
        )

        return paginate(items)
