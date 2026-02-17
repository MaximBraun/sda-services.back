# coding utf-8

from typing import Callable, Any

from datetime import date as date_type

from sqlalchemy import (
    Result,
    ScalarResult,
    Executable,
    ColumnElement,
    select,
    insert,
    delete,
    update,
    and_,
    func,
)

from sqlalchemy.orm import (
    selectinload,
    with_loader_criteria,
)

from .base import ISchema

from .table import ITable

from .engine import IEngine


class IRepository:
    def __init__(
        self,
        engine: IEngine,
        model: ITable,
    ) -> None:
        self._engine = engine
        self._model = model

    async def __commit_changes(
        self,
        query: Executable,
    ) -> None:
        async with self._engine.get_session() as session:
            await session.execute(
                query,
            )
            await session.commit()

    async def __session_result(
        self,
        query: Executable,
    ) -> ScalarResult | None:
        async with self._engine.get_session() as session:
            result: Result = await session.execute(
                query,
            )
            return result.scalars()

    async def __fetch_records(
        self,
        query: Executable,
        many: bool = True,
    ) -> list[Any] | Any | None:
        scalars: ScalarResult = await self.__session_result(
            query,
        )
        return scalars.all() if many else scalars.first()

    async def fetch_all(
        self,
    ) -> list[Any] | None:
        return await self.__fetch_records(
            select(self._model),
        )

    def __filter_one_to_many(
        self,
        related: list[str],
        models: list[object] | None = None,
        filters_by_model: dict[object, Callable] | None = None,
    ):
        options = []

        for rel in related:
            parts = rel.split(".")
            # начинаем с первой связи от self._model
            current = selectinload(getattr(self._model, parts[0]))
            option = current
            model = self._model

            # дальше углубляемся во вложенные связи
            for part in parts[1:]:
                rel_model = getattr(model, parts[0]).property.mapper.class_
                current = current.selectinload(getattr(rel_model, part))
                model = rel_model
                parts.pop(0)

            options.append(option)

        if filters_by_model and models is not None:
            for model in models:
                if model in filters_by_model:
                    options.append(with_loader_criteria(model, filters_by_model[model]))

        return select(self._model).options(*options)

    async def fetch_one_to_many(
        self,
        field: str | None = None,
        value: str | None = None,
        many: bool = True,
        *args,
        **kwargs,
    ):
        stmt = self.__filter_one_to_many(*args, **kwargs)
        if field and value is not None:
            stmt = stmt.where(getattr(self._model, field) == value)
        return await self.__fetch_records(stmt, many=many)

    async def fetch_one(
        self,
    ) -> Any | None:
        return await self.__fetch_records(
            select(self._model),
            many=False,
        )

    async def fetch_field(
        self,
        field_name: str,
        value: Any,
        many: bool = True,
    ) -> Any | None:
        condition: ColumnElement = getattr(self._model, field_name)
        return await self.__fetch_records(
            select(self._model).where(
                condition.in_(value) if isinstance(value, list) else condition == value
            ),
            many=many,
        )

    async def add_record(
        self,
        data: ISchema,
    ) -> ISchema:
        await self.__commit_changes(
            insert(self._model).values(
                **data.dict,
            ),
        )
        return data

    async def update_record(
        self,
        id: int,
        data: ISchema | dict[str, ...],
    ) -> ISchema:
        await self.__commit_changes(
            update(self._model)
            .filter_by(id=id)
            .values(
                **data.dict if not isinstance(data, dict) else data,
            ),
        )
        return data

    async def delete_record(
        self,
        id: int,
    ) -> bool:
        await self.__commit_changes(
            delete(self._model).filter_by(
                id=id,
            ),
        )
        return True

    async def fetch_one_with_filters(
        self,
        where: str,
        value: str,
        order_by: str,
        many: bool = False,
    ):
        return await self.__fetch_records(
            select(self._model)
            .where(getattr(self._model, where) == value)
            .order_by(getattr(self._model, order_by))
            .limit(1),
            many=many,
        )

    async def fetch_with_filters(
        self,
        many: bool = False,
        **filters: str,
    ) -> list[Any] | Any | None:
        conditions = [
            func.date(getattr(self._model, f)) == v
            if isinstance(v, date_type)
            else getattr(self._model, f) == v
            for f, v in filters.items()
            if v is not None
        ]

        return await self.__fetch_records(
            select(self._model).where(and_(*conditions)), many=many
        )

    async def fetch_one_with_filter(
        self,
        order_by: str,
        many: bool = False,
        **filters: str,
    ):
        conditions = [
            getattr(self._model, field) == value for field, value in filters.items()
        ]
        return await self.__fetch_records(
            select(self._model)
            .where(and_(*conditions))
            .order_by(getattr(self._model, order_by))
            .limit(1),
            many=many,
        )
