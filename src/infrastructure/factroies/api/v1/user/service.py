# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import AuthUserRepository

from ......interface.controllers.api.v1 import UserServiceController

from .....api.views.v1 import UserServiceView


class AuthUserRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> AuthUserRepository:
        return AuthUserRepository(
            IDatabase(
                conf,
            ),
        )


class UserServiceControllerFactory:
    @staticmethod
    def get(
        repository: AuthUserRepository = Depends(
            AuthUserRepositoryFactory.get,
        ),
    ) -> UserServiceController:
        return UserServiceController(
            repository,
        )


class UserServiceViewFactory:
    @staticmethod
    def create(
        controller: UserServiceController = Depends(
            UserServiceControllerFactory.get,
        ),
    ) -> UserServiceView:
        return UserServiceView(
            controller,
        )
