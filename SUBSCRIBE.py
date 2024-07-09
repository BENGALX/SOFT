import logging
import re
import contextlib
from telethon.tl import functions
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class RaffleMod(loader.Module):
    """Модуль рафлер деф.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL DEF"}

    def channels(self, text):
        links = []
        for word in text.split():
            if word.startswith("https://t.me/"):
                links.append(word)
            elif word.startswith("http://t.me/"):
                links.append(word)
        return links

    def re_chennel(self, text):
        ms = re.findall(r'<a\s+[^>]*href=["\'](https?://[^"\']+)', text)
        return list(ms) if ms else False

    def re_usernames(self, text):
        uss = []
        pattern = r"@(\w+)"
        matches = re.findall(pattern, text)
        uss.extend(iter(matches))
        return uss or False

    @loader.watcher(only_channels=True)
    async def subscribe_to_channel(self, message):
        chat = utils.get_chat_id(message)
        if chat != 2035849227:
            return
        links_to_subscribe, usernames_to_subscribe = self.channels(message.text)
        ms = self.re_chennel(message.text)
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

