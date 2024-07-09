import logging
from telethon.tl import functions
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class UNSUBMod(loader.Module):
    """Модуль отписок от каналов.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BENGAL UNSUBSCRIBE"}

    async def send_unsubscribe_message(self, chat_id, channel_name):
        text = f"Вы успешно отписались от канала {channel_name}"
        await self.client.send_message(chat_id, text)

    @loader.watcher(only_channels=True)
    async def unsubscribe_channel(self, message):
        chat = message.chat_id
        if chat != -1002035849227:
            return
        if not message.text.startswith("@"):
            return
        try:
            await self.client(functions.channels.LeaveChannelRequest(message.text))
            await self.send_unsubscribe_message(message.chat_id, message.text)
        except Exception as e:
            await self.client.delete_dialog(message.text)
            logger.error(f"Failed to unsubscribe from channel: {e}")
        else:
            logger.info("Unsubscribed from channel")
