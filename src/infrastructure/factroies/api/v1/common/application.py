# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import ApplicationRepository

from ......interface.controllers.api.v1 import ApplicationController

from .....api.views.v1 import ApplicationView


class ApplicationRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> ApplicationRepository:
        return ApplicationRepository(
            IDatabase(
                conf,
            ),
        )


class ApplicationControllerFactory:
    @staticmethod
    def get(
        repository: ApplicationRepository = Depends(
            ApplicationRepositoryFactory.get,
        ),
    ) -> ApplicationController:
        return ApplicationController(
            repository,
        )


class ApplicationViewFactory:
    @staticmethod
    def create(
        controller: ApplicationController = Depends(
            ApplicationControllerFactory.get,
        ),
    ) -> ApplicationView:
        return ApplicationView(
            controller,
        )
