# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PixverseApplicationRepository

from ......interface.controllers.api.v1 import PixverseApplicationController

from .....api.views.v1 import PixverseApplicationView


class PixverseApplicationRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PixverseApplicationRepository:
        return PixverseApplicationRepository(
            IDatabase(
                conf,
            ),
        )


class PixverseApplicationControllerFactory:
    @staticmethod
    def get(
        repository: PixverseApplicationRepository = Depends(
            PixverseApplicationRepositoryFactory.get,
        ),
    ) -> PixverseApplicationController:
        return PixverseApplicationController(
            repository,
        )


class PixverseApplicationViewFactory:
    @staticmethod
    def create(
        controller: PixverseApplicationController = Depends(
            PixverseApplicationControllerFactory.get,
        ),
    ) -> PixverseApplicationView:
        return PixverseApplicationView(
            controller,
        )
