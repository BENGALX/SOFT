import logging
from telethon.tl import functions, types
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class AutoReactMod(loader.Module):
    """Автоматически ставит реакции"""

    strings = {"name": "AutoReact"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "channel_id",
                [],
                lambda: "ID каналов, в которых будет участвовать модуль",
                validator=loader.validators.Series(
                    loader.validators.Union(
                        loader.validators.Integer(),
                    )
                ),
            ),
        )

    async def auto_react(self, message):
        chat = utils.get_chat_id(message)
        if chat in self.config["channel_id"]:
            try:
                await self.client(functions.messages.SendReactionRequest(
                    peer=chat,
                    id=[message.id],
                    reaction='👍'  # Замените на любую желаемую реакцию
                ))
                logger.info(f'Reacted to message {message.id} in channel {chat}')
            except Exception as e:
                logger.error(f'Failed to react to message {message.id} in channel {chat}: {e}')

    @loader.watcher(only_channels=True)
    async def reaction_watcher(self, message: types.Message):
        await self.auto_react(message)
