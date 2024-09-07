import re
from .. import loader, utils
from telethon.tl.types import PeerChannel

@loader.tds
class RunnerMod(loader.Module):
    """Модуль нажатия деф кнопок.
           Commands: /run.\n
    ⚙️ By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL-RUNNER"}

    async def process_private_link(self, link):
        link = link.split("//t.me/c/")[1]
        link = link.split("/")
        privat_message = f"<b>Вы нажали кнопку в розыгрыше:</b>\n https://t.me/c/{link[0]}/{link[1]}"
        b_msg = await self.client.get_messages(PeerChannel(int(link[0])), ids=int(link[1]))
        click = await b_msg.click(data=b_msg.reply_markup.rows[0].buttons[0].data)
        await self.send_me_message(privat_message)

    async def process_public_link(self, link):
        link = link.split("//t.me/")[1]
        link = link.split("/")
        public_message = f"<b>Вы нажали кнопку в розыгрыше:</b>\n https://t.me/{link[0]}/{link[1]}"
        b_msg = await self.client.get_messages(link[0], ids=int(link[1]))
        click = await b_msg.click(data=b_msg.reply_markup.rows[0].buttons[0].data)
        await self.send_me_message(public_message)

    async def send_me_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != -1002371391894:
            return
        try:
            if message.message.startswith("/run"):
                private_links = re.findall(r'https?://t.me/c/.*/.*', message.message)
                public_links = re.findall(r'https?://t.me/.*/.*', message.message)
                
                for link in private_links:
                    await self.process_private_link(link)
                for link in public_links:
                    await self.process_public_link(link)
        except:
            pass
