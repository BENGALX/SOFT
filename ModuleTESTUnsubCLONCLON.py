# meta developer: @pavlyxa_rezon
# meta_private: This module is written for personal use, and is not intended for public use, do not distribute it

import logging
from telethon.tl import functions
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class RaffleMod(loader.Module):
    """Тестим"""

    strings = {"name": "TESTUnsubClon"}

    @loader.watcher(only_channels=True)
    async def unsubscribe_channel(self, message):
        chat = message.chat_id
        if chat != -1002035849227:
            return
        if not message.text.startswith("@"):
            return
        try:
            await self.client(functions.channels.LeaveChannelRequest(message.text))
        except Exception as e:
            await self.client.delete_dialog(message.text)
        else:
            logger.info("Unsubscribed from channel")
