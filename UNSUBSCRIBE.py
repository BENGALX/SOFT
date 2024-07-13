import logging
from telethon.tl import functions
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class UNSUBMod(loader.Module):
    """Модуль отписок от каналов.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_UNSUBSCR"}

    async def send_bot_message(self, text):
        await self.client.send_message('me', text)

    @loader.watcher(only_channels=True)
    async def unsubscribe_channel(self, message):
        chat = message.chat_id
        success_message = f"<b>Вы успешно отписались от:</b> {message.text}"
        if chat != -1002035849227:
            return
        if not message.text.startswith("@"):
            return
        try:
            await self.client(functions.channels.LeaveChannelRequest(message.text))
            await self.send_bot_message(success_message)
        except Exception as e:
            await self.client.delete_dialog(message.text)
            logger.error(f"Failed to unsubscribe. {e}")
        else:
            logger.info("Unsubscribed from channel.")
