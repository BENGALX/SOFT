import re
from .. import loader, utils
from telethon.tl.types import PeerChannel

@loader.tds
class RunnerMod(loader.Module):
    """Модуль нажатия INL кнопок.
           Commands: /run.\n
    ⚙️ By @pavlyxa_rezon"""

    strings = {"name": "BGL-RUNNER"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_uid", -1002205010643, "CustomID",
                validator=loader.validators.Integer(),
            )
        )

    async def process_private_link(self, link):
        link = link.split("//t.me/c/")[1]
        link = link.split("/")
        privat_message = f"<b>Вы нажали кнопку в розыгрыше:</b>\n https://t.me/c/{link[0]}/{link[1]}"
        inline_button = await self.client.get_messages(PeerChannel(int(link[0])), ids=int(link[1]))
        click = await inline_button.click(data=inline_button.reply_markup.rows[0].buttons[0].data)
        await self.send_me_message(privat_message)

    async def process_public_link(self, link):
        link = link.split("//t.me/")[1]
        link = link.split("/")
        public_message = f"<b>Вы нажали кнопку в розыгрыше:</b>\n https://t.me/{link[0]}/{link[1]}"
        inline_button = await self.client.get_messages(link[0], ids=int(link[1]))
        click = await inline_button.click(data=inline_button.reply_markup.rows[0].buttons[0].data)
        await self.send_me_message(public_message)

    async def send_me_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    async def handle_run_command(self, message):
        private_links = re.findall(r'https?://t.me/c/.*/.*', message.message)
        public_links = re.findall(r'https?://t.me/.*/.*', message.message)
                
        for link in private_links:
            await self.process_private_link(link)
        for link in public_links:
            await self.process_public_link(link)

    @loader.watcher()
    async def watcher_group(self, message):
        if message.chat_id != self.config["custom_uid"]:
            return
        try:
            if message.message.startswith("/run"):
                await self.handle_run_command(message)
        except:
            pass
