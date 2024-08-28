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

    async def unsubscribe_by_tag(self, target):
        done_message = f"<b>Вы успешно отписались от</b> {target}"
        user_message = f"<b>Вы успешно удалили чат с</b> {target}"
        try:
            await self.client(functions.channels.LeaveChannelRequest(target))
            await self.send_me_message(done_message)
        except:
            await self.client.delete_dialog(target)
            await self.send_me_message(user_message)

    async def unsubscribe_by_link(self, target):
        match = re.search(r't\.me/([a-zA-Z0-9_]+)', target)
        done_message = f"<b>Вы успешно отписались от</b>\n{target}"
        user_message = f"<b>Вы успешно удалили чат с</b>\n{target}"
        if match:
            username = match.group(1)
            try:
                await self.client(functions.channels.LeaveChannelRequest(username))
                await self.send_me_message(done_message)
            except:
                await self.client.delete_dialog(username)
                await self.send_me_message(user_message)
        else:
            await self.send_me_message("Не удалось извлечь имя пользователя.")

    async def unsubscribe_by_id(self, target):
        done_message = f"<b>Вы успешно отписались от ID:</b>{target}"
        user_message = f"<b>Вы успешно удалили чат с ID:</b> {target}"
        try:
            channel_id = int(target)
            await self.client(functions.channels.LeaveChannelRequest(channel_id))
            await self.send_me_message(done_message)
        except:
            await self.client.delete_dialog(channel_id)
            await self.send_me_message(user_message)

    @loader.watcher()
    async def watcher_group(self, message):
        if message.chat_id != -1002205010643:
            return

        if message.text.startswith("/uns"):
            target = message.text.split("/uns", 1)[1].strip()
            fail_message = f"<b>Цель удаления не распознана:</b> {target}"
            if target.startswith("@"):
                await self.unsubscribe_by_tag(target)
            elif "t.me/" in target:
                await self.unsubscribe_by_link(target)
            elif target.isdigit():
                await self.unsubscribe_by_id(target)
            else:
                await self.send_me_message(fail_message)
