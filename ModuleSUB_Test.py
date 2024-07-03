# meta developer: @pavlyxa_rezon
# meta_private: This module is written for personal use, and is not intended for public use, do not distribute it

import contextlib
import logging
from telethon.tl import functions, types
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class RaffleMod(loader.Module):
    """Подписываться на каналы"""

    strings = {"name": "BGL SUBSCR"}

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

    @loader.watcher(only_channels=True)
    async def subscribe_to_channel(self, message):
        chat = utils.get_chat_id(message)
        if chat != -1002037892569:
            return
        links_to_subscribe, usernames_to_subscribe = self.channels(message.text)
        with contextlib.suppress(Exception):
            if links_to_subscribe:
                for link in links_to_subscribe:
                    await self.client(functions.channels.JoinChannelRequest(link))
            if usernames_to_subscribe:
                for username in usernames_to_subscribe:
                    await self.client(functions.channels.JoinChannelRequest(username))
            if ms:
                for m in ms:
                    logging.info(m)
                    await self.client(functions.channels.JoinChannelRequest(m))
            if "/joinchat/" in message.text:
                ghash = message.text.split("/joinchat/")[1]
                await self.client(functions.messages.ImportChatInviteRequest(ghash))
                
            if message.text.startswith("https://t.me/+"):
                await message.client(
                    functions.channels.JoinChannelRequest(message.text)
                )
