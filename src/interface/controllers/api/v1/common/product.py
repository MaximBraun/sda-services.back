# coding utf-8

from ......infrastructure.orm.database.repositories import ProductRepository

from ......interface.schemas.api import (
    Product,
    IProduct,
)


class ProductController:
    def __init__(
        self,
        repository: ProductRepository,
    ) -> None:
        self._repository = repository

    async def fetch_products(
        self,
    ) -> list[Product]:
        return await self._repository.fetch_all()

    async def fetch_product(
        self,
        id: int,
    ) -> Product:
        return await self._repository.fetch_application(
            "id",
            id,
        )

    async def add_product(
        self,
        data: IProduct,
    ) -> IProduct:
        return await self._repository.add_record(
            data,
        )

    async def delete_product(
        self,
        id: int,
    ) -> bool:
        return await self._repository.delete_record(
            id,
        )

    async def update_product(
        self,
        id: int,
        data: IProduct,
    ) -> IProduct:
        return await self._repository.update_record(
            id,
            data,
        )
