import re
from telethon.tl.types import Message
from telethon.tl.functions.messages import StartBotRequest
from .. import loader

@loader.tds
class ReferalMod(loader.Module):
    """Модуль участия в рефках.
           Commands: /ref.\n
    ⚙️ By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL-REFERAL"}

    async def start_bestrandom_bot(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            ref_key = match[1]
            await self.client(StartBotRequest(bot="BestRandom_bot", peer="BestRandom_bot", start_param=ref_key))

    async def start_fastes_bot(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            ref_key = match[1]
            await self.client(StartBotRequest(bot="TheFastes_Bot", peer="TheFastes_Bot", start_param=ref_key))

    async def start_fastesru_bot(self, text):
        if match := re.search(r"\?start=(\w+)", text):
            ref_key = match[1]
            await self.client(StartBotRequest(bot="TheFastesRuBot", peer="TheFastesRuBot", start_param=ref_key))

    async def start_givelucky_bot(self, text):
        if match := re.search(r"\?start=([\w-]+)", text):
            ref_key = match[1]
            await self.client(StartBotRequest(bot="GiveawayLuckyBot", peer="GiveawayLuckyBot", start_param=ref_key))
    
    async def send_me_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    @loader.watcher(only_channels=True)
    async def watcher_bot(self, message: Message):
        if message.chat_id != -1002371391894:
            return
        if message.text.startswith("/ref"):
            linka = message.text.split("/ref", 1)[1].strip()
            done_message = f"<b>Вы успешно стартанули рефку:</b> \n {linka}"
            fail_message = f"<b>Введена неправильная ссылка:</b> \n {linka}"
            
            if "BestRandom_bot" in message.text:
                await self.start_bestrandom_bot(message.text)
                await self.send_me_message(done_message)

            elif "TheFastes_Bot" in message.text:
                await self.start_fastes_bot(message.text)
                await self.send_me_message(done_message)

            elif "TheFastesRuBot" in message.text:
                await self.start_fastesru_bot(message.text)
                await self.send_me_message(done_message)

            elif "GiveawayLuckyBot" in message.text:
                await self.start_givelucky_bot(message.text)
                await self.send_me_message(done_message)

            else:
                await self.send_me_message(fail_message)
