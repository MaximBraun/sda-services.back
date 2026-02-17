# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import UserDataRepository

from ......interface.controllers.api.v1 import UserDataController

from .....api.views.v1 import UserDataView


class UserDataRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> UserDataRepository:
        return UserDataRepository(
            IDatabase(
                conf,
            ),
        )


class UserDataControllerFactory:
    @staticmethod
    def get(
        repository: UserDataRepository = Depends(
            UserDataRepositoryFactory.get,
        ),
    ) -> UserDataController:
        return UserDataController(
            repository,
        )


class UserDataViewFactory:
    @staticmethod
    def create(
        controller: UserDataController = Depends(
            UserDataControllerFactory.get,
        ),
    ) -> UserDataView:
        return UserDataView(
            controller,
        )
