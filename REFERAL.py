import re
from telethon.tl.types import Message
from telethon.tl.functions.messages import StartBotRequest
from .. import loader

@loader.tds
class ReferalMod(loader.Module):
    """Модуль участия в рефках.
           Commands: /best, /fast, /faru, /give.\n
    ⚙️ By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL-REFERAL"}

    async def start_bestrandom_bot(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            ref_key = match[1]
            linka = text.split("/best", 1)[1].strip()
            success_message = f"<b>Вы успешно стартанули рефку:</b> \n {linka}"
            await self.client(StartBotRequest(bot="BestRandom_bot", peer="BestRandom_bot", start_param=ref_key))
            await self.send_me_message(success_message)

    async def start_fastes_bot(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            ref_key = match[1]
            linka = text.split("/fast", 1)[1].strip()
            success_message = f"<b>Вы успешно стартанули рефку:</b> \n {linka}"
            await self.client(StartBotRequest(bot="TheFastes_Bot", peer="TheFastes_Bot", start_param=ref_key))
            await self.send_me_message(success_message)

    async def start_fastesru_bot(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            ref_key = match[1]
            linka = text.split("/faru", 1)[1].strip()
            success_message = f"<b>Вы успешно стартанули рефку:</b> \n {linka}"
            await self.client(StartBotRequest(bot="TheFastesRuBot", peer="TheFastesRuBot", start_param=ref_key))
            await self.send_me_message(success_message)

    async def start_givelucky_bot(self, text):
        if match := re.search(r"\?start=([\w-]+)", text):
            ref_key = match[1]
            linka = text.split("/give", 1)[1].strip()
            success_message = f"<b>Вы успешно стартанули рефку:</b> \n {linka}"
            await self.client(StartBotRequest(bot="GiveawayLuckyBot", peer="GiveawayLuckyBot", start_param=ref_key))
            await self.send_me_message(success_message)
    
    async def send_me_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    @loader.watcher(only_channels=True)
    async def watcher_bot(self, message: Message):
        if message.chat_id != -1002156895908:
            return
        if message.text.startswith("/best"):
            await self.start_bestrandom_bot(message.text)
        if message.text.startswith("/fast"):
            await self.start_fastes_bot(message.text)
        if message.text.startswith("/faru"):
            await self.start_fastesru_bot(message.text)
        if message.text.startswith("/give"):
            await self.start_givelucky_bot(message.text)
