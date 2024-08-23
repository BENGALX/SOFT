from telethon.tl.functions.messages import SendMessageRequest
from .. import loader

@loader.tds
class PovtoratorMod(loader.Module):
    """Модуль для вывода сообщений.
           Команда: /comanda.\n
    ⚙️ By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL-POVTORATOR"}

    async def send_message(self, chat_id, message_text):
        try:
            chat_entity = await self._client.get_entity(chat_id)
            await self._client(SendMessageRequest(peer=chat_entity, message=message_text))
        except:
            pass

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != -1002205010643:
            return
        try:
            if message.message.startswith("/comanda"):
                message_text = message.text.split("/comanda", 1)[1].strip()
                await self.send_message(-1002205010643, message_text)
        except:
            pass
