# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PikaApplicationRepository

from ......interface.controllers.api.v1 import PikaApplicationController

from .....api.views.v1 import PikaApplicationView


class PikaApplicationRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PikaApplicationRepository:
        return PikaApplicationRepository(
            IDatabase(
                conf,
            ),
        )


class PikaApplicationControllerFactory:
    @staticmethod
    def get(
        repository: PikaApplicationRepository = Depends(
            PikaApplicationRepositoryFactory.get,
        ),
    ) -> PikaApplicationController:
        return PikaApplicationController(
            repository,
        )


class PikaApplicationViewFactory:
    @staticmethod
    def create(
        controller: PikaApplicationController = Depends(
            PikaApplicationControllerFactory.get,
        ),
    ) -> PikaApplicationView:
        return PikaApplicationView(
            controller,
        )
