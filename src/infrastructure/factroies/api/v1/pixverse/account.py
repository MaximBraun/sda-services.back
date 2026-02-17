# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PixverseAccountRepository

from ......interface.controllers.api.v1 import PixverseAccountController

from .....api.views.v1 import PixverseAccountView


class PixverseAccountRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PixverseAccountRepository:
        return PixverseAccountRepository(
            IDatabase(
                conf,
            ),
        )


class PixverseAccountControllerFactory:
    @staticmethod
    def get(
        repository: PixverseAccountRepository = Depends(
            PixverseAccountRepositoryFactory.get,
        ),
    ) -> PixverseAccountController:
        return PixverseAccountController(
            repository,
        )


class PixverseAccountViewFactory:
    @staticmethod
    def create(
        controller: PixverseAccountController = Depends(
            PixverseAccountControllerFactory.get,
        ),
    ) -> PixverseAccountView:
        return PixverseAccountView(
            controller,
        )
