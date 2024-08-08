import logging
import re
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class StealerMod(loader.Module):
    """Модуль для ловли чеков.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_STEALER"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chat_id", 2219293691, "ID",
                validator=loader.validators.Integer(),
            )
        )

    async def message_q(self, text: str, user_id: int):
        async with self.client.conversation(user_id) as conv:
            msg = await conv.send_message(text)
            response = await conv.get_response()
            if '⏳' in response.text:
                await conv.get_response()
            return response

    @loader.watcher()
    async def watcher(self, message):
        try:
            if message.peer_id.channel_id == self.config["chat_id"]:
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    answer = ""
                    for link in links:
                        u = link.split('?start=')
                        ind = u[0].index('me/') + 3
                        cbot = f'@{u[0][ind:]}'.replace("send", "CryptoBot")
                        try:
                            await self.message_q(f'/start {u[1]}', cbot)
                            answer = answer + "Successfully" + "\n"
                        except:
                            answer = answer + "Unsuccessfully" + "\n"
                        await utils.answer(message, answer)
        except:
            pass
