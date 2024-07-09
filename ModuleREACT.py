# meta developer: @your_username
# meta_private: This module is written for personal use, and is not intended for public use, do not distribute it

import logging
import random
from telethon.tl import functions, types
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class AutoReactMod(loader.Module):
    """Автоматически ставит положительные реакции на последние посты в привязанном канале"""

    strings = {"name": "AutoReact"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "channel_id",
                -1002035849227,
                lambda: "ID канала, в котором будет работать модуль",
                validator=loader.validators.Integer()
            )
        )
        self.reactions = ['👍', '❤️', '🔥']  # Положительные реакции

    async def auto_react(self, message):
        chat = utils.get_chat_id(message)
        logger.info(f'Checking message {message.id} in chat {chat}')
        if chat == self.config["channel_id"]:
            try:
                reaction = random.choice(self.reactions)
                await self.client(functions.messages.SendReactionRequest(
                    peer=chat,
                    id=[message.id],
                    reaction=[reaction]
                ))
                logger.info(f'Reacted with {reaction} to message {message.id} in channel {chat}')
            except Exception as e:
                logger.error(f'Failed to react to message {message.id} in channel {chat}: {e}')
        else:
            logger.info(f'Message {message.id} is not in the configured channel {self.config["channel_id"]}')

    @loader.watcher(only_channels=True)
    async def reaction_watcher(self, message: types.Message):
        logger.info(f'New message {message.id} in chat {utils.get_chat_id(message)}')
        await self.auto_react(message)

    async def client_ready(self, client, db):
        self.client = client
        logger.info('AutoReactMod is ready')
