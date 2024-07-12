import logging
import re
from telethon.tl.types import Message
from telethon.tl.functions.messages import StartBotRequest
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class RefkaMod(loader.Module):
    """Модуль участия в рефках.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_REFKA"}

    async def start_the_fastest_bot(self, param):
        await self._client(
            StartBotRequest(
                bot="TheFastesRuBot", peer="TheFastesRuBot", start_param=param
            )
        )
        logging.info(f"Bot started ref: {param} for TheFastesRuBot")

    async def start_best_random_bot(self, param):
        await self._client(
            StartBotRequest(
                bot="BestRandom_bot", peer="BestRandom_bot", start_param=param
            )
        )
        logging.info(f"Bot started ref: {param} for BestRandom_bot")

    async def start_default_bot(self, param):
        await self._client(
            StartBotRequest(
                bot="TheFastes_Bot", peer="TheFastes_Bot", start_param=param
            )
        )
        logging.info(f"Bot started ref: {param} for default bot")

    async def attempt_to_start(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            param = match[1]

            logging.info(f"Bot started ref: {param}")
            logging.info("TEXT: " + text)

            if "TheFastesRuBot" in text:
                await self.start_the_fastest_bot(param)
            elif "BestRandom_bot" in text:
                await self.start_best_random_bot(param)
            else:
                await self.start_default_bot(param)

    @loader.watcher(only_channels=True)
    async def watcher_bot(self, message: Message):
        if message.chat_id != -1002219293691:
            return

        await self.attempt_to_start(message.text)
