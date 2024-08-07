import logging
from telethon.tl.functions.messages import SendMessageRequest
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class MessageSenderMod(loader.Module):
    """Модуль для отправки смс в чат.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_MESSAGE_SENDER"}

    async def send_message(self, chat_username, message_text):
        try:
            chat_entity = await self._client.get_entity(chat_username)
            await self._client(SendMessageRequest(peer=chat_entity, message=message_text))
            logger.info(f"Message sent to {chat_username}: {message_text}")
        except Exception as e:
            logger.error(f"Error sending message to {chat_username}: {e}")

    @loader.command("sms", aliases=["sendmessage"])
    async def send_message_command(self, message):
        args = message.text.split(" ", 2)
        if len(args) < 3:
            await message.respond("Usage: /sms <chat_username> <message_text>")
            return
        chat_username, message_text = args[1], args[2]
        await self.send_message(chat_username, message_text)
        await message.respond(f"Message sent to {chat_username}: {message_text}")
