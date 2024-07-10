import logging
import re
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class SUBMod(loader.Module):
    """Модуль подписок на каналы.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_SUBSCR"}

    @loader.watcher()
    async def watcher(self, message):
        chat_id = 2035849227
        try:
            if message.peer_id.channel_id == chat_id:
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    for link in links:
                        try:
                            await self.client(JoinChannelRequest(channel=link))
                        except:
                            await self.client(ImportChatInviteRequest(link.split("t.me/+")[1]))
        except:
            pass
        try:
            if message.peer_id.chat_id == chat_id:
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    for link in links:
                        try:
                            await self.client(JoinChannelRequest(channel=link))
                        except:
                            await self.client(ImportChatInviteRequest(link.split("t.me/+")[1]))
        except:
            pass
