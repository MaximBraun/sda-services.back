# coding utf-8

from fastapi_pagination import (
    Page,
    paginate,
)

from ......infrastructure.orm.database.models import Services

from ......infrastructure.orm.database.repositories import ServiceRepository

from .....schemas.api import (
    ServiceRoute,
)


class UserRouteController:
    def __init__(
        self,
        repository: ServiceRepository,
    ) -> None:
        self._repository = repository

    async def fetch_routes(
        self,
        title: str,
    ) -> Page[ServiceRoute]:
        service: Services = await self._repository.fetch_with_filters(
            title=title,
        )

        items: list[ServiceRoute] = list(
            map(
                lambda route: ServiceRoute.model_validate(route),
                service.routes,
            )
        )

        return paginate(items)
