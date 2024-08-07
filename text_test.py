import logging
from telethon import events
from .. import loader

logger = logging.getLogger(name)

@loader.tds
class SendBotMessageMod(loader.Module):
    """Модуль для отправки сообщений в бота по команде /smscb.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "SendBotMessage"}
    
    async def send_bot_message(self, bot_id, text):
        await self.client.send_message(bot_id, text)

    @loader.on(events.NewMessage(pattern='/smscb (.+)'))
    async def handler(self, event):
        chat_id = 2035849227  # ваш привязанный чат
        bot_id = 1559501630   # айди бота
        if event.chat_id == chat_id:
            text = event.pattern_match.group(1)
            try:
                await self.send_bot_message(bot_id, text)
                await event.respond(f"Сообщение '{text}' успешно отправлено в бота.")
            except Exception as e:
                logger.error(f"Error sending message to bot: {e}")
                await event.respond(f"Произошла ошибка при отправке сообщения в бота: {e}")
