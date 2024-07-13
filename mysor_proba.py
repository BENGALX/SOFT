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

            if "BestRandom_bot" in text:
                await self._client(
                    StartBotRequest(
                        bot="BestRandom_bot", peer="BestRandom_bot", start_param=param
                    )
                )

            if "TheFastes_Bot" in text:
                await self._client(
                    StartBotRequest(
                        bot="TheFastes_Bot", peer="TheFastes_Bot", start_param=param
                    )
                )

    @loader.watcher(only_channels=True)
    async def watcher_bot(self, message: Message):
        if message.chat_id != -1002219293691:
            return

        await self.attempt_to_start(message.text)
