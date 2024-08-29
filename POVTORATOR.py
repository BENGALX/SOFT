from telethon.tl.functions.messages import SendMessageRequest
from .. import loader

@loader.tds
class PovtoratorMod(loader.Module):
    """Модуль для вывода сообщений.
           Команда: /comanda.\n
    ⚙️ By @pavlyxa_rezon"""

    strings = {"name": "BGL-POVTORATOR"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_uid", -1002205010643, "CustomID",
                validator=loader.validators.Integer(),
            )
        )

    async def send_message(self, chat_id, message_text):
        try:
            chat_entity = await self.client.get_entity(chat_id)
            await self.client(SendMessageRequest(peer=chat_entity, message=message_text))
        except:
            pass

    async def handle_command(self, text):
        message_text = text.split("/comanda", 1)[1].strip()
        chat_id = self.config["custom_uid"]
        await self.send_message(chat_id, message_text)

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != self.config["custom_uid"]:
            return
        if message.text.startswith("/comanda"):
            await self.handle_command(message.text)
