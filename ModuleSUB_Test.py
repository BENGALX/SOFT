# meta developer: @pavlyxa_rezon
# meta_private: This module is written for personal use, and is not intended for public use, do not distribute it

import logging
from telethon.tl import functions, types
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class SubscriptionMod(loader.Module):
    """Подписываться на каналы"""

    strings = {"name": "BENGAL_SUBSCR"}

    def __init__(self):
        self.config = loader.ModuleConfig()

    def channels(self, text):
        links = []
        for word in text.split():
            if word.startswith("https://t.me/") or word.startswith("http://t.me/"):
                links.append(word)
        return links

    @loader.watcher(only_channels=True)
    async def subscribe_to_channel(self, message: types.Message):
        chat = utils.get_chat_id(message)
        if chat != -1002037892569:
            return
        links_to_subscribe = self.channels(message.text)
        if links_to_subscribe:
            for link in links_to_subscribe:
                try:
                    await message.client(functions.channels.JoinChannelRequest(link))
                except Exception as error:
                    logger.info(f"Failed to join {link}: {error}")
