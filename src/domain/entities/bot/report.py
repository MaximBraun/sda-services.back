# coding utf-8

from aiogram.exceptions import TelegramAPIError

from aiogram.enums.parse_mode import ParseMode

from .bot import IBot

from ..core import IConfEnv


class IBotReporter:
    def __init__(
        self,
        conf: IConfEnv,
    ) -> None:
        self._bot = IBot(
            conf,
        )

    async def send_error(
        self,
        text: str,
    ) -> None:
        try:
            await self._bot.telegram_bot.send_message(
                chat_id=self._bot._conf.telegram_chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
            )
        except TelegramAPIError as err:
            raise err

    async def send_error_message(
        self,
        text: str,
    ) -> None:
        return await self.send_error(
            text,
        )
