# coding utf-8

from fastapi import Depends

from ......domain.conf import app_conf

from ......domain.repositories import IDatabase

from ......domain.entities.core import IConfEnv

from .....orm.database.repositories import TopmediaVoiceRepository

from ......interface.controllers.api.v1 import TopmediaVoiceController

from .....api.views.v1 import TopmediaVoiceView


class TopmediaVoiceRepositoryFactory:
    @staticmethod
    def get(
        conf: IConfEnv = Depends(app_conf),
    ) -> TopmediaVoiceRepository:
        return TopmediaVoiceRepository(
            IDatabase(
                conf,
            ),
        )


class TopmediaVoiceControllerFactory:
    @staticmethod
    def get(
        repository: TopmediaVoiceRepository = Depends(
            TopmediaVoiceRepositoryFactory.get,
        ),
    ) -> TopmediaVoiceController:
        return TopmediaVoiceController(
            repository,
        )


class TopmediaVoiceViewFactory:
    @staticmethod
    def create(
        controller: TopmediaVoiceController = Depends(
            TopmediaVoiceControllerFactory.get,
        ),
    ) -> TopmediaVoiceView:
        return TopmediaVoiceView(
            controller,
        )
