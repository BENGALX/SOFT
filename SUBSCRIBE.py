import re
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from .. import loader

@loader.tds
class SUBMod(loader.Module):
    """Модуль подписок на каналы.
           Commands: /sub.\n
    ⚙️ By BENGAL & @pavlyxa_rezon\n"""

    strings = {"name": "BGL-SUBSCRIBE"}
    
    async def send_me_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    async def subscribe_by_link(self, link):
        done_message = f"<b>Вы успешно подписались на:</b>\n {link}"
        fail_message = f"<b>Не удалось подписаться на:</b>\n {link}"
        try:
            await self.client(JoinChannelRequest(channel=link))
            await self.send_me_message(done_message)
        except:
            try:
                invite_hash = link.split("t.me/+")[1]
                await self.client(ImportChatInviteRequest(invite_hash))
                await self.send_me_message(done_message)
            except:
                await self.send_me_message(fail_message)

    async def handle_subscribe(self, text):
        link = text.split("/sub", 1)[1].strip()
        await self.subscribe_by_link(link)

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != -1002205010643:
            return
            
        if message.message.startswith("/sub"):
            await self.handle_subscribe(message.message)
