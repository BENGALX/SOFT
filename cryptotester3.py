# meta developer: @SNEGIREKgg

import asyncio
import logging
import re
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class RefRunMod(loader.Module):
    """Модуль для упрощения выполнения реф. системы"""

    strings = {"name": "RefRun"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chat_id",
                2205010643, # jog
                "ID чата в который ты будешь кидать ссылки",
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
                        cbot = cbot.replace("xrocket", "tonRocketBot")
                        try:
                            await self.message_q(f'/start {u[1]}', cbot)
                            answer = answer + "Successfully" + "\n"
                        except:
                            answer = answer + "Unsuccessfully" + "\n"
                        await utils.answer(message, answer)
        except:
            pass
        try:
            if message.peer_id.chat_id == self.config["chat_id"]:
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    answer = ""
                    for link in links:
                        u = link.split('?start=')
                        ind = u[0].index('me/') + 3
                        cbot = f'@{u[0][ind:]}'.replace("send", "CryptoBot")
                        cbot = cbot.replace("xrocket", "tonRocketBot")
                        try:
                            await self.message_q(f'/start {u[1]}', cbot)
                            answer = answer + "Successfully" + "\n"
                        except:
                            answer = answer + "Unsuccessfully" + "\n"
                        await utils.answer(message, answer)
        except:
            pass
