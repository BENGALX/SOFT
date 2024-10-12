import re
import aiohttp
import asyncio
from .. import loader, utils

@loader.tds
class GiveShareMod(loader.Module):
    """Модуль для запуска GiveShare бота.
           Команды: /giveshare link\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {"name": "GiveShare"}

    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643

    async def start_giveshare_app(self, ref_key):
        """Запуск веб-приложения GiveShare через HTTP-запрос."""
        try:
            app_url = f"https://t.me/GiveShareBot/app?startapp={ref_key}"
            async with aiohttp.ClientSession() as session:
                async with session.get(app_url) as response:
                    if response.status == 200:
                        await self.send_module_message(f"<b>✅ Открыто веб-приложение:</b> {app_url}")
                    else:
                        await self.send_module_message(f"<b>🚫 Ошибка при открытии веб-приложения:</b> {response.status}")
        except Exception as e:
            error_message = f"<b>🚫 Ошибка открытия веб-приложения:</b> {e}"
            await self.send_module_message(error_message)

    async def handle_referral(self, text):
        """Обработка команды /giveshare.""" 
        match = re.search(r"startapp=([\w-]+)", text)
        if match:
            ref_key = match.group(1)
            await self.start_giveshare_app(ref_key)
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
