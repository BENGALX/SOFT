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
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_uid", -1002205010643, "CustomID",
                validator=loader.validators.Integer(),
            )
        )

    async def send_me_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    async def subscribe_by_link(self, target):
        done_message = f"<b>Вы успешно подписались на:</b>\n {target}"
        fail_message = f"<b>Не удалось подписаться на:</b>\n {target}"
        try:
            await self.client(JoinChannelRequest(channel=target))
            await self.send_me_message(done_message)
        except:
            try:
                invite_hash = target.split("t.me/+")[1]
                await self.client(ImportChatInviteRequest(invite_hash))
                await self.send_me_message(done_message)
            except:
                await self.send_me_message(fail_message)

    async def handle_subscribe(self, text):
        target = text.split("/sub", 1)[1].strip()
        await self.subscribe_by_link(target)

    @loader.watcher()
    async def watcher_group(self, message):
        if message.chat_id != self.config["custom_uid"]:
            return

        try:
            if message.message.startswith("/sub"):
                await self.handle_subscribe(message.message)
        except:
            pass
