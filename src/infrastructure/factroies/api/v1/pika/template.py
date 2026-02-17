# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PikaTemplateRepository

from ......interface.controllers.api.v1 import PikaTemplateController

from .....api.views.v1 import PikaTemplateView


class PikaTemplateRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PikaTemplateRepository:
        return PikaTemplateRepository(
            IDatabase(
                conf,
            ),
        )


class PikaTemplateControllerFactory:
    @staticmethod
    def get(
        repository: PikaTemplateRepository = Depends(
            PikaTemplateRepositoryFactory.get,
        ),
    ) -> PikaTemplateController:
        return PikaTemplateController(
            repository,
        )


class PikaTemplateViewFactory:
    @staticmethod
    def create(
        controller: PikaTemplateController = Depends(
            PikaTemplateControllerFactory.get,
        ),
    ) -> PikaTemplateView:
        return PikaTemplateView(
            controller,
        )
