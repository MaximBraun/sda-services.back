# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PixverseStyleRepository

from ......interface.controllers.api.v1 import PixverseStyleController

from .....api.views.v1 import PixverseStyleView


class PixverseStyleRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PixverseStyleRepository:
        return PixverseStyleRepository(
            IDatabase(
                conf,
            ),
        )


class PixverseStyleControllerFactory:
    @staticmethod
    def get(
        repository: PixverseStyleRepository = Depends(
            PixverseStyleRepositoryFactory.get,
        ),
    ) -> PixverseStyleController:
        return PixverseStyleController(
            repository,
        )


class PixverseStyleViewFactory:
    @staticmethod
    def create(
        controller: PixverseStyleController = Depends(
            PixverseStyleControllerFactory.get,
        ),
    ) -> PixverseStyleView:
        return PixverseStyleView(
            controller,
        )
