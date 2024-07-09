import random
import asyncio
from telethon.tl import functions

from .. import loader, utils

@loader.tds
class ReactionModule(loader.Module):
    """Модуль для ставки рандомных положительных реакций на посты в канале"""

    def __init__(self):
        self.config = loader.ModuleConfig(
            "target_channel_id",
            [],
            "Айди канала, на который будут ставиться реакции",
            lambda x: list(map(int, x.split())),
        )

    @loader.watcher(only_incoming=True, pattern=r".*")
    async def watch_and_react(self, message):
        chat_id = message.chat_id
        if chat_id not in self.config["target_channel_id"]:
            return

        try:
            await message.client(functions.messages.AddReactionRequest(
                message.chat_id,
                message.id,
                random.choice(['👍', '❤️', '😊'])
            ))
        except Exception as e:
            print(f"Ошибка при добавлении реакции: {e}")

