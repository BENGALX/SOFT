from telethon.tl import functions
from .. import loader

@loader.tds
class UNSUBMod(loader.Module):
    """Модуль отписок от каналов.
           Commands: /uns.\n
    ⚙️ By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL-UNSUBSCR"}

    async def send_me_message(self, text):
        await self.client.send_message('me', text)

    @loader.watcher()
    async def unsubscribe_channel(self, message):

        if message.chat_id != -1002371391894:
            return
            
        if message.text.startswith("/uns"):
            tag = message.text.split("/uns", 1)[1].strip()
            done_message = f"<b>Вы успешно отписались от</b> {tag}"
            else_message = f"<b>Вы успешно удалили чат с</b> {tag}"
            
            if tag.startswith("@"):
                try:
                    await self.client(functions.channels.LeaveChannelRequest(tag))
                    await self.send_me_message(done_message)
                except:
                    await self.client.delete_dialog(tag)
                    await self.send_me_message(else_message)
