import re
import asyncio
import webbrowser
from .. import loader, utils

from telethon.tl import functions
from telethon.tl.types import Message, PeerChannel
from telethon.tl.functions.messages import StartBotRequest

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

    async def start_giveshare_app(self, ref_key):
        """Запуск веб-приложения GiveShare с реферальным ключом."""
        try:
            app_url = f"https://t.me/GiveShareBot/app?startapp={ref_key}"
            webbrowser.open(app_url)  # Открываем URL в браузере
            await self.send_module_message(f"<b>✅ Открыто веб-приложение:</b> {app_url}")
        except Exception as e:
            error_message = f"<b>🚫 Ошибка открытия веб-приложения:</b> {e}"
            await self.send_module_message(error_message)

    async def handle_referral(self, text):
        """Обработка команды /giveshare для запуска веб-приложения."""
        match = re.search(r"startapp=([\w-]+)", text)
        if match:
            ref_key = match.group(1)
            await self.start_giveshare_app(ref_key)  # Изменили вызов метода
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
