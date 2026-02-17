# coding utf-8

from ......interface.controllers.api.v1 import ProductController

from ......interface.schemas.api import (
    Product,
    IProduct,
)


class ProductView:
    def __init__(
        self,
        controller: ProductController,
    ) -> None:
        self._controller = controller

    async def fetch_products(
        self,
    ) -> list[Product]:
        return await self._controller.fetch_products()

    async def fetch_product(
        self,
        id: int,
    ) -> Product:
        return await self._controller.fetch_product(
            id,
        )

    async def add_product(
        self,
        data: IProduct,
    ) -> IProduct:
        return await self._controller.add_product(
            data,
        )

    async def update_product(
        self,
        id: int,
        data: IProduct,
    ) -> IProduct:
        return await self._controller.update_product(
            id,
            data,
        )

    async def delete_product(
        self,
        id: int,
    ) -> bool:
        return await self._controller.delete_product(
            id,
        )
