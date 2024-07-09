import logging
from telethon.tl import functions
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class UNSUBMod(loader.Module):
    """Модуль отписок от каналов.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_UNSUBSCR"}

    async def send_unsubscribe_message(self, chat_id, channel_name):
        text = f"<b>Вы успешно отписались от {channel_name}</b>"
        await self.inline.bot.send_message(chat_id, text=text, parse_mode="html")

    @loader.watcher(only_channels=True)
    async def unsubscribe_channel(self, message):
        chat = message.chat_id
        if chat != -1002035849227:
            return
        if not message.text.startswith("@"):
            return
        try:
            await self.client(functions.channels.LeaveChannelRequest(message.text))
            await self.send_unsubscribe_message(self.tg_id, message.text)
        except Exception as e:
            await self.client.delete_dialog(message.text)
            logger.error(f"Failed to unsubscribe from channel. {e}")
        else:
            logger.info("Unsubscribed from channel.")
