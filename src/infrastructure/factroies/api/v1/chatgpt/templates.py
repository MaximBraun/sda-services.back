# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import PhotoGeneratorTemplateRepository

from ......interface.controllers.api.v1 import PhotoGeneratorTemplateController

from .....api.views.v1 import PhotoGeneratorTemplateView


class PhotoGeneratorTemplateRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> PhotoGeneratorTemplateRepository:
        return PhotoGeneratorTemplateRepository(
            IDatabase(
                conf,
            ),
        )


class PhotoGeneratorTemplateControllerFactory:
    @staticmethod
    def get(
        repository: PhotoGeneratorTemplateRepository = Depends(
            PhotoGeneratorTemplateRepositoryFactory.get,
        ),
    ) -> PhotoGeneratorTemplateController:
        return PhotoGeneratorTemplateController(
            repository,
        )


class PhotoGeneratorTemplateViewFactory:
    @staticmethod
    def create(
        controller: PhotoGeneratorTemplateController = Depends(
            PhotoGeneratorTemplateControllerFactory.get,
        ),
    ) -> PhotoGeneratorTemplateView:
        return PhotoGeneratorTemplateView(
            controller,
        )
