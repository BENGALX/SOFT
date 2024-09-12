from telethon.tl.functions.account import GetAuthorizationsRequest
from telethon.tl.functions.messages import SendMessageRequest
from .. import loader

@loader.tds
class StatusAccMod(loader.Module):
    """Модуль для получения информации о твине.
           Команда: /status.\n
    ⚙️ By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL-STATUSACC"}

    async def send_status(self, chat_id):
        try:
            user = await self.client.get_me()

            first_name = user.first_name
            last_name = user.last_name
            full_name = f"{first_name} {last_name}"
            username = f"@{user.username}" if user.username else "NONE"
            phone = user.phone if user.phone else "Нет номера"
            user_id = user.id

            sessions = await self.client(GetAuthorizationsRequest())
            session_count = len(sessions.authorizations)
            session_info = "\n".join(
                [
                    f"├{s.device_model}"
                    for s in sessions.authorizations[:-1]
                ]
            )
            session_info += f"\n└{sessions.authorizations[-1].device_model}"

            status_message = (
                f"TWINK — {full_name}\n"
                f"├USER: {username}\n"
                f"├NUM: +{phone}\n"
                f"└UID: {user_id}\n"
                f"\n"
                f"SESSIONS — {session_count}\n{session_info}"
            )

            await self.client(SendMessageRequest(peer=chat_id, message=status_message))
        except Exception as e:
            await self.client.send_message(chat_id, f"⚠️ Ошибка: {str(e)}")

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != -1002231264660:
            return
        try:
            if message.message.startswith("/status"):
                parts = message.message.split()
                if len(parts) == 1:
                    await self.send_status(message.chat_id)
                elif len(parts) == 2:
                    requested_tag = parts[1]
                    user = await self.client.get_me()
                    if requested_tag == f"@{user.username}":
                        await self.send_status(message.chat_id)
        except Exception as e:
            await self.client.send_message(message.chat_id, f"⚠️ Ошибка в watcher: {str(e)}")
