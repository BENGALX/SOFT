import random
import re
import asyncio
from telethon import events
from .. import loader
from telethon.tl.types import PeerChannel

@loader.tds
class ReactorMod(loader.Module):
    """Модуль для автореакций.
           Commands: /react <L>, /stopreaction, /startreaction.\n
    ⚙️ By @pavlyxa_rezon\n"""
  
    strings = {"name": "BGL-REACTOR"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "command_uid", -1002205010643, "ID группы для команд",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "newreact_uid", -1001833137041, "Каналы для авто-реакций",
                validator=loader.validators.Integer(),
            )
        )

        self.reactions = ["👍", "😊", "😁", "😎", "🔥", "💪", "👌", "👏", 
                          "🎉", "❤️‍🔥", "❤️", "😇", "🙏", "💯", "⚡️", "💪", "🏆"]
        self.auto_reactions_enabled = True

    async def process_private_link(self, link, reaction):
        link = link.split("//t.me/c/")[1]
        link = link.split("/")
        channel_id = int(link[0])
        message_id = int(link[1])
        try:
            msg = await self.client.get_messages(PeerChannel(channel_id), ids=message_id)
            await msg.react(reaction)
            await self.client.send_message('me', f"✅ Реакция {reaction} на: https://t.me/c/{link[0]}/{link[1]}")
        except:
            pass

    async def process_public_link(self, link, reaction):
        link = link.split("//t.me/")[1]
        link = link.split("/")
        username = link[0]
        message_id = int(link[1])
        try:
            msg = await self.client.get_messages(username, ids=message_id)
            await msg.react(reaction)
            await self.client.send_message('me', f"✅ Реакция {reaction} на: https://t.me/{link[0]}/{link[1]}")
        except:
            pass

    async def handle_react_command(self, message):
        reaction = random.choice(self.reactions)
        private_links = re.findall(r'https?://t.me/c/.*/.*', message.message)
        public_links = re.findall(r'https?://t.me/.*/.*', message.message)
        for link in private_links:
            await self.process_private_link(link, reaction)
        for link in public_links:
            await self.process_public_link(link, reaction)

    @loader.watcher()
    async def watcher_group(self, message):
        if message.chat_id != self.config["command_uid"]:
            return
        try:
            if message.message.startswith("/react"):
                await self.handle_react_command(message)
            if message.message.startswith("/stopreaction"):
                self.auto_reactions_enabled = False
                await message.respond("⚠️ Авто-реакции отключены.")
            if message.message.startswith("/startreaction"):
                self.auto_reactions_enabled = True
                await message.respond("✅ Авто-реакции включены.")
        except:
            pass

        if message.chat_id != self.config["newreact_uid"] or not self.auto_reactions_enabled:
            return
        try:
            keywords = ["шоп", "приним", "заказ", "эмбл", "набор", "вход", "акция", "отзыв", "магаз", "реакц", "забы", "участ"]
            if any(keyword in message.message.lower() for keyword in keywords):
                random_reaction = random.choice(self.reactions)
                msg = await self.client.get_messages(message.chat_id, ids=message.id)
                await msg.react(random_reaction)
                await asyncio.sleep(3)
        except:
            pass
