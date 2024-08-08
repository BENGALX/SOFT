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
                link = message.text.split(" ", 1)[1]
                u = link.split('?start=')
                ind = u[0].index('me/') + 3
                cbot = f'@{u[0][ind:]}'.replace("send", "CryptoBot")
                try:
                    await self.mess(f'/start {u[1]}', cbot)
                    await utils.answer(message, "Чек активирован!")
                except:
                    await utils.answer(message, "Ошибка, проверьте ссылку.")
        except:
            pass
