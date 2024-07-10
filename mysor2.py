import asyncio
import logging
import re
from .. import loader, utils
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

logger = logging.getLogger(__name__)

@loader.tds
class SUBMod(loader.Module):
    """Модуль подписок на каналы.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_SUBSCR"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chat_id", 2035849227, "ID",
                validator=loader.validators.Integer(),
            )
        )

    async def send_subscribe_message(self, chat_id):
        text = "<b>Вы подписались на канал</b>"
        await self.client.send_message(chat_id, text=text, parse_mode="html")

    @loader.watcher()
    async def watcher(self, message):
        try:
            if message.peer_id.channel_id == self.config["chat_id"]:
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    for link in links:
                        try:
                            await self.client(JoinChannelRequest(channel=link))
                            await self.send_subscribe_message(message.chat_id)
                        except:
                            await self.client(ImportChatInviteRequest(link.split("t.me/+")[1]))
                            await self.send_subscribe_message(message.chat_id)
        except:
            pass
        try:
            if message.peer_id.chat_id == self.config["chat_id"]:
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    for link in links:
                        try:
                            await self.client(JoinChannelRequest(channel=link))
                            await self.send_subscribe_message(message.chat_id)
                        except:
                            await self.client(ImportChatInviteRequest(link.split("t.me/+")[1]))
                            await self.send_subscribe_message(message.chat_id)
        except:
            pass
