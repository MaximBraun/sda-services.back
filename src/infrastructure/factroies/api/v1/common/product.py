# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import ProductRepository

from ......interface.controllers.api.v1 import ProductController

from .....api.views.v1 import ProductView


class ProductRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> ProductRepository:
        return ProductRepository(
            IDatabase(
                conf,
            ),
        )


class ProductControllerFactory:
    @staticmethod
    def get(
        repository: ProductRepository = Depends(
            ProductRepositoryFactory.get,
        ),
    ) -> ProductController:
        return ProductController(
            repository,
        )


class ProductViewFactory:
    @staticmethod
    def create(
        controller: ProductController = Depends(
            ProductControllerFactory.get,
        ),
    ) -> ProductView:
        return ProductView(
            controller,
        )
