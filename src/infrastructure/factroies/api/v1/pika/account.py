# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PikaAccountRepository

from ......interface.controllers.api.v1 import PikaAccountController

from .....api.views.v1 import PikaAccountView


class PikaAccountRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PikaAccountRepository:
        return PikaAccountRepository(
            IDatabase(
                conf,
            ),
        )


class PikaAccountControllerFactory:
    @staticmethod
    def get(
        repository: PikaAccountRepository = Depends(
            PikaAccountRepositoryFactory.get,
        ),
    ) -> PikaAccountController:
        return PikaAccountController(
            repository,
        )


class PikaAccountViewFactory:
    @staticmethod
    def create(
        controller: PikaAccountController = Depends(
            PikaAccountControllerFactory.get,
        ),
    ) -> PikaAccountView:
        return PikaAccountView(
            controller,
        )
