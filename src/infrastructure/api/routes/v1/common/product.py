# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)

from ....views.v1 import ProductView

from ......domain.tools import (
    validate_token,
)

from .....factroies.api.v1 import ProductViewFactory

from ......interface.schemas.api import (
    Product,
    IProduct,
)


product_router = APIRouter(tags=["Appstore Products"])


@product_router.get(
    "/products",
)
async def fetch_products(
    _: str = Depends(validate_token),
    view: ProductView = Depends(
        ProductViewFactory.create,
    ),
) -> list[Product]:
    return await view.fetch_products()


@product_router.get(
    "/products/{id}",
)
async def fetch_product(
    id: int,
    _: str = Depends(validate_token),
    view: ProductView = Depends(
        ProductViewFactory.create,
    ),
) -> Product:
    return await view.fetch_product(
        id,
    )


@product_router.post(
    "/products",
)
async def add_product(
    data: IProduct,
    _: str = Depends(validate_token),
    view: ProductView = Depends(
        ProductViewFactory.create,
    ),
) -> IProduct:
    return await view.add_product(
        data,
    )


@product_router.put(
    "/products/{id}",
)
async def update_product(
    id: int,
    data: IProduct,
    _: str = Depends(validate_token),
    view: ProductView = Depends(
        ProductViewFactory.create,
    ),
) -> IProduct:
    return await view.update_product(
        id,
        data,
    )


@product_router.delete(
    "/products/{id}",
)
async def delete_product(
    id: int,
    _: str = Depends(validate_token),
    view: ProductView = Depends(
        ProductViewFactory.create,
    ),
) -> bool:
    return await view.delete_product(
        id,
    )
