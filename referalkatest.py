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

    async def start_the_fastes_bot(self, key):
        await self._client(
            StartBotRequest(
                bot="TheFastesRuBot", peer="TheFastesRuBot", start_ref=key
            )
        )

    async def start_best_random_bot(self, key):
        await self._client(
            StartBotRequest(
                bot="BestRandom_bot", peer="BestRandom_bot", start_ref=key
            )
        )

    async def start_the_fastes_bot(self, key):
        await self._client(
            StartBotRequest(
                bot="TheFastes_Bot", peer="TheFastes_Bot", start_ref=key
            )
        )

    async def attempt_to_start(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            key = match[1]
            logging.info(f"Bot started ref: {key}")

            if "TheFastesRuBot" in text:
                await self.start_the_fastest_bot(key)
            if "BestRandom_bot" in text:
                await self.start_best_random_bot(key)
            if "BestRandom_bot" in text:
                await self.start_the_fastes_bot(key)

    @loader.watcher(only_channels=True)
    async def watcher_bot(self, message: Message):
        if message.chat_id != -1002219293691:
            return
        await self.attempt_to_start(message.text)
