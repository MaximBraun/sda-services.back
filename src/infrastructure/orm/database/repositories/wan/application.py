# coding utf-8

from sqlalchemy import delete, insert

from ...models import (
    WanApplications,
    WanTemplates,
)

from ......domain.repositories import (
    IDatabase,
    DatabaseRepository,
)


class WanApplicationRepository(DatabaseRepository):
    def __init__(
        self,
        engine: IDatabase,
    ) -> None:
        super().__init__(
            engine,
            WanApplications,
        )

    async def fetch_all(
        self,
        related: list[str],
    ) -> WanApplications:
        return await self.fetch_one_to_many(
            related=related,
        )

    async def fetch_application(
        self,
        field_name: str,
        value: str,
        related: list[str],
    ) -> WanApplications | None:
        return await self.fetch_one_to_many(
            field_name,
            value,
            many=False,
            related=related,
            models=(WanTemplates,),
            filters_by_model={
                WanTemplates: lambda v: v.is_active,
            },
        )

    async def update_application(
        self,
        application_id: int,
        relation_table,
        relation_ids: list[int],
        relation_column_name: str,
    ):
        async with self._engine.get_session() as session:
            await session.execute(
                delete(relation_table).where(
                    relation_table.c.application_id == application_id
                )
            )

            if relation_ids:
                await session.execute(
                    insert(relation_table),
                    [
                        {"application_id": application_id, relation_column_name: rel_id}
                        for rel_id in relation_ids
                    ],
                )

            await session.commit()
