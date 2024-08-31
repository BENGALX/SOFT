from telethon.tl.functions.messages import SendMessageRequest
from .. import loader

@loader.tds
class MessagerMod(loader.Module):
    """Модуль для рассылки SMS в чаты.
           Commands: /sms.\n
    ⚙️ By @pavlyxa_rezon"""

    strings = {"name": "BGL-MESSAGER"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_uid", -1002205010643, "CustomID",
                validator=loader.validators.Integer(),
            )
        )
  
    async def send_message(self, chat_username, message_text):
        done_message = f"<b>В чат {chat_username} успешно отправлена рассылка:</b>\n {message_text}"
        fail_message = f"<b>Не удалось отправить в {chat_username} рассылку:</b>\n {message_text}"
        try:
            chat_entity = await self.client.get_entity(chat_username)
            await self.client(SendMessageRequest(peer=chat_entity, message=message_text))
            await self.send_me_message(done_message)
        except:
            await self.send_me_message(fail_message)

    async def send_me_message(self, text):
        await self.client.send_message('me', text)

    async def handle_sms_command(self, message):
        args = message.text.split(" ", 2)
        if len(args) < 3:
            return
        chat_username, message_text = args[1], args[2]
        if not chat_username.startswith("@"):
            return
        await self.send_message(chat_username, message_text)

    @loader.watcher()
    async def watcher_group(self, message):
        if message.chat_id != self.config["custom_uid"]:
            return
        
        if message.text.startswith("/sms"):
            await self.handle_sms_command(message)
