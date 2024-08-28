from telethon.tl import functions
from .. import loader
import re

@loader.tds
class UNSUBMod(loader.Module):
    """Модуль для автоудаления.
           Commands: /uns.\n
    ⚙️ By @pavlyxa_rezon"""

    strings = {"name": "BGL-UNSUBSCR"}

    async def send_me_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    @loader.watcher()
    async def unsubscribe_channel(self, message):
        if message.chat_id != -1002187149618:
            return

        if message.text.startswith("/uns"):
            target = message.text.split("/uns", 1)[1].strip()
            
            done_message = f"<b>Вы успешно отписались от</b> {target}"
            user_message = f"<b>Вы успешно удалили чат с</b> {target}"
            fail_message = f"<b>Цель удаления не распознана</b> {target}"

            if target.startswith("@"):
                try:
                    await self.client(functions.channels.LeaveChannelRequest(target))
                    await self.send_me_message(done_message)
                except:
                    await self.client.delete_dialog(target)
                    await self.send_me_message(user_message)
            elif "t.me/" in target:
                match = re.search(r't\.me/([a-zA-Z0-9_]+)', target)
                if match:
                    username = match.group(1)
                    try:
                        await self.client(functions.channels.LeaveChannelRequest(username))
                        await self.send_me_message(done_message)
                    except:
                        await self.client.delete_dialog(username)
                        await self.send_me_message(user_message)
                else:
                    await self.send_me_message(f"Не вышло извлечь имя пользователя.")
            elif target.isdigit():
                try:
                    channel_id = int(target)
                    await self.client(functions.channels.LeaveChannelRequest(channel_id))
                    await self.send_me_message(done_message)
                except:
                    await self.client.delete_dialog(channel_id)
                    await self.send_me_message(user_message)
            else:
                await self.send_me_message(fail_message)
