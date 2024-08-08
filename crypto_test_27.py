import logging
import re
from .. import loader, utils

logger = logging.getLogger(__name__)

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

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != -1002205010643:
            return
        try:
            if message.text.startswith("/check"):
                link = re.search(r'http[s]?://t.me/[^?\s]+', message.text)
                if link:
                    u = link.group()
                    ind = u.index('me/') + 3
                    cbot = f'@{u[ind:]}'.replace("send", "CryptoBot")
                    try:
                        await self.mess(f'/start {u}', cbot)
                        await utils.answer(message, "Чекактивирован!")
                    except:
                        await utils.answer(message, "Ошибка.")
        except:
            pass
