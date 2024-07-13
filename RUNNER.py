import asyncio
import logging
import re
from .. import loader, utils
from telethon.tl.types import PeerChannel

logger = logging.getLogger(__name__)

@loader.tds
class RunnerMod(loader.Module):
    """Модуль нажатия деф кнопок.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_RUNNER"}

    async def process_links(self, message):
        links = re.findall(r'https?://t.me/c/.*/.*', message.message)
        links1 = re.findall(r'https?://t.me/.*/.*', message.message)
        
        for link in links:
            link = link.split("//t.me/c/")[1]
            link = link.split("/")
            privat_message = f"<b>Вы успешно участвуете в розыгрыше:</b> \n https://t.me/c/{link[0]}/{link[1]}"
            b_msg = await self.client.get_messages(PeerChannel(int(link[0])), ids=int(link[1]))
            click = await b_msg.click(data=b_msg.reply_markup.rows[0].buttons[0].data)
            await self.send_bot_message(privat_message)
        
        for link in links1:
            link = link.split("//t.me/")[1]
            link = link.split("/")
            public_message = f"<b>Вы успешно участвуете в розыгрыше:</b> \n https://t.me/{link[0]}/{link[1]}"
            b_msg = await self.client.get_messages(link[0], ids=int(link[1]))
            click = await b_msg.click(data=b_msg.reply_markup.rows[0].buttons[0].data)
            await self.send_bot_message(public_message)
        
    async def send_bot_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    @loader.watcher()
    async def watcher(self, message):
        try:
            if hasattr(message.peer_id, 'channel_id') and message.peer_id.channel_id == 2239254863:
                if "t.me/" in message.message:
                    await self.process_links(message)
        except Exception as e:
            logger.error(f"Error in watcher: {e}")
