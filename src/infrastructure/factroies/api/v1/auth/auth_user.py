# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import AuthUserRepository

from ......interface.controllers.api.v1 import AuthUserController

from .....api.views.v1 import AuthUserView


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


class AuthUserControllerFactory:
    @staticmethod
    def get(
        repository: AuthUserRepository = Depends(
            AuthUserRepositoryFactory.get,
        ),
    ) -> AuthUserController:
        return AuthUserController(
            repository,
        )


class AuthUserViewFactory:
    @staticmethod
    def create(
        controller: AuthUserController = Depends(
            AuthUserControllerFactory.get,
        ),
    ) -> AuthUserView:
        return AuthUserView(
            controller,
        )
