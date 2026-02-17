# coding utf-8

from asyncio import gather

from ...models import PixverseStyles

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class PixverseStyleRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            PixverseStyles,
        )

    async def fetch_style(
        self,
        field_name: str,
        value: str | int,
    ) -> PixverseStyles | None:
        return await self.fetch_field(
            field_name,
            value,
            many=False,
        )

    async def fetch_styles_by_id(
        self,
        data: list[int],
    ) -> list[PixverseStyles]:
        return await gather(
            *[
                self.fetch_style(
                    "id",
                    id,
                )
                for id in data
            ]
        )
