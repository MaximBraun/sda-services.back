# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import ServiceRepository

from ......interface.controllers.api.v1 import UserRouteController

from .....api.views.v1 import UserRouteView


class ServiceRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> ServiceRepository:
        return ServiceRepository(
            IDatabase(
                conf,
            ),
        )


class UserRouteControllerFactory:
    @staticmethod
    def get(
        repository: ServiceRepository = Depends(
            ServiceRepositoryFactory.get,
        ),
    ) -> UserRouteController:
        return UserRouteController(
            repository,
        )


class UserRouteViewFactory:
    @staticmethod
    def create(
        controller: UserRouteController = Depends(
            UserRouteControllerFactory.get,
        ),
    ) -> UserRouteView:
        return UserRouteView(
            controller,
        )
