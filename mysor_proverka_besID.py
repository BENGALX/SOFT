import asyncio
import logging
import re
from .. import loader, utils
from telethon.tl.types import PeerChannel

logger = logging.getLogger(__name__)

@loader.tds
class RunButtonMod(loader.Module):
    """Модуль нажатия деф кнопок.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_RUNNER_DEF"}

    async def process_links(self, message):
        links = re.findall(r'https?://t.me/c/.*/.*', message.message)
        links1 = re.findall(r'https?://t.me/.*/.*', message.message)
        answer = ""
        for link in links:
            link = link.split("//t.me/c/")[1]
            link = link.split("/")
            b_msg = await self._client.get_messages(PeerChannel(int(link[0])), ids=int(link[1]))
            click = await b_msg.click(data=b_msg.reply_markup.rows[0].buttons[0].data)
            answer = answer + click.message + "\n"
        for link in links1:
            link = link.split("//t.me/")[1]
            link = link.split("/")
            b_msg = await self._client.get_messages(link[0], ids=int(link[1]))
            click = await b_msg.click(data=b_msg.reply_markup.rows[0].buttons[0].data)
            answer = answer + click.message + "\n"
        await utils.answer(message, answer)

    @loader.watcher()
    async def watcher(self, message):
        try:
            if hasattr(message.peer_id, 'channel_id') and message.peer_id.channel_id == 2035849227:
                if "t.me/" in message.message:
                    await self.process_links(message)
        except Exception as e:
            logger.error(f"Error in watcher: {e}")
