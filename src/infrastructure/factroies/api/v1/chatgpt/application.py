# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PhotoGeneratorApplicationRepository

from ......interface.controllers.api.v1 import PhotoGeneratorApplicationController

from .....api.views.v1 import PhotoGeneratorApplicationView


class PhotoGeneratorApplicationRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PhotoGeneratorApplicationRepository:
        return PhotoGeneratorApplicationRepository(
            IDatabase(
                conf,
            ),
        )


class PhotoGeneratorApplicationControllerFactory:
    @staticmethod
    def get(
        repository: PhotoGeneratorApplicationRepository = Depends(
            PhotoGeneratorApplicationRepositoryFactory.get,
        ),
    ) -> PhotoGeneratorApplicationController:
        return PhotoGeneratorApplicationController(
            repository,
        )


class PhotoGeneratorApplicationViewFactory:
    @staticmethod
    def create(
        controller: PhotoGeneratorApplicationController = Depends(
            PhotoGeneratorApplicationControllerFactory.get,
        ),
    ) -> PhotoGeneratorApplicationView:
        return PhotoGeneratorApplicationView(
            controller,
        )
