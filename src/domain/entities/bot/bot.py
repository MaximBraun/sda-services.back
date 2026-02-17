# coding utf-8

from functools import cached_property

from aiogram import (
    Bot,
    Dispatcher,
)

from ..core import IConfEnv


class IBot:
    def __init__(
        self,
        conf: IConfEnv,
    ) -> None:
        self._conf = conf

    @cached_property
    def telegram_bot(
        self,
    ) -> Bot:
        return Bot(
            token=self._conf.telegram_bot_token,
        )

    def set_dispatcher(
        self,
    ) -> Dispatcher:
        return Dispatcher(
            bots=self.telegram_bot,
        )
