import logging
import re
from .. import loader, utils

logger = logging.getLogger(name)

@loader.tds
class StealerMod(loader.Module):
    """Модуль для ловли чеков.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_STEALER"}

    async def mess(self, text: str, user_id: int):
        async with self.client.conversation(user_id) as conv:
            msg = await conv.send_message(text)
            response = await conv.get_response()
            if '⏳' in response.text:
                await conv.get_response()
            return response

    async def send_bot_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != -1002205010643:
            return
        try:
            if "/check" in message.message:
                links = re.findall(r'https?://t.me/.*', message.message)
                for link in links:
                    u = link.split('?start=')
                    ref_code = u[1]
                    cbot = "@CryptoBot"
                    try:
                        await self.mess(f'/start {ref_code}', cbot)
                        await self.send_bot_message(f"Чек активирован: {link}")
                    except:
                        pass
        except:
            pass
