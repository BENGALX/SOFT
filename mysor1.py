# meta developer: @pavlyxa_rezon
# meta_private: This module is written for personal use, and is not intended for public use, do not distribute it

import contextlib
import logging
import asyncio
import re
from telethon.tl import functions, types
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class RaffleMod(loader.Module):
    """Тестим"""

    strings = {"name": "TESTUnsubClon"}

    def channels(self, text):
        links = []
        usernames = []
        for word in text.split():
            logger.info(word)
            if word.startswith("@"):
                usernames.append(word)
            elif word.startswith("https://t.me/"):
                links.append(word)
            elif word.startswith("http://t.me/"):
                links.append(word)
        return links, usernames

    def extract_channel_and_post_id(self, text):
        # https://t.me/username/123 -> username, 123
        reg = re.compile(r"https://t.me/([^/]+)/(\d+)")
        return (match[1], match[2]) if (match := reg.search(text)) else False

    @loader.watcher(only_channels=True)
    async def unsubscribe_channel(self, message):
        chat = message.chat_id
        if chat != -1002035849227:
            return
        try:
            await self.client(functions.channels.LeaveChannelRequest(message.text))
        except Exception as e:
            await self.client.delete_dialog(message.text)
        else:
            logger.info("Unsubscribed from channel")
