# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import QwenAccountRepository

from ......interface.controllers.api.v1 import QwenAccountController

from .....api.views.v1 import QwenAccountView


class QwenAccountRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> QwenAccountRepository:
        return QwenAccountRepository(
            IDatabase(
                conf,
            ),
        )


class QwenAccountControllerFactory:
    @staticmethod
    def get(
        repository: QwenAccountRepository = Depends(
            QwenAccountRepositoryFactory.get,
        ),
    ) -> QwenAccountController:
        return QwenAccountController(
            repository,
        )


class QwenAccountViewFactory:
    @staticmethod
    def create(
        controller: QwenAccountController = Depends(
            QwenAccountControllerFactory.get,
        ),
    ) -> QwenAccountView:
        return QwenAccountView(
            controller,
        )
