# meta developer: @pavlyxa_rezon
# meta_private: This module is written for personal use, and is not intended for public use, do not distribute it

import logging
import re

from telethon.tl.types import Message
from telethon.tl.functions.messages import StartBotRequest

from .. import loader

logger = logging.getLogger(__name__)


@loader.tds
class FastBot(loader.Module):
    """Для BestRandom и FastBot"""

    strings = {"name": "BGL REF"}

    async def attempt_to_start(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            param = match[1]

            logging.info(f"Bot started ref: {param}")
            logging.info("TEXT: " + text)

            if "TheFastesRuBot" in text:
                await self._client(
                    StartBotRequest(
                        bot="TheFastesRuBot", peer="TheFastesRuBot", start_param=param
                    )
                )
                logging.info(f"Bot started ref: {param}")
                return

            elif "BestRandom_bot" in text:
                await self._client(
                    StartBotRequest(
                        bot="BestRandom_bot", peer="BestRandom_bot", start_param=param
                    )
                )
                logging.info(f"Bot started ref: {param}")
                return

            await self._client(
                StartBotRequest(
                    bot="TheFastes_Bot", peer="TheFastes_Bot", start_param=param
                )
            )

            logging.info(f"Bot started ref: {param}")

    @loader.watcher(only_channels=True)
    async def watcher_bot(self, message: Message):
        if message.chat_id != -1001974431455:
            return

        await self.attempt_to_start(message.text)
