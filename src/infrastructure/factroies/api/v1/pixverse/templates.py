# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PixverseTemplateRepository

from ......interface.controllers.api.v1 import PixverseTemplateController

from .....api.views.v1 import PixverseTemplateView


class PixverseTemplateRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PixverseTemplateRepository:
        return PixverseTemplateRepository(
            IDatabase(
                conf,
            ),
        )


class PixverseTemplateControllerFactory:
    @staticmethod
    def get(
        repository: PixverseTemplateRepository = Depends(
            PixverseTemplateRepositoryFactory.get,
        ),
    ) -> PixverseTemplateController:
        return PixverseTemplateController(
            repository,
        )


class PixverseTemplateViewFactory:
    @staticmethod
    def create(
        controller: PixverseTemplateController = Depends(
            PixverseTemplateControllerFactory.get,
        ),
    ) -> PixverseTemplateView:
        return PixverseTemplateView(
            controller,
        )
