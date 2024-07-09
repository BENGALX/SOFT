import logging
import re
from telethon.tl import functions, types
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class ChannelSubscribeMod(loader.Module):
    """Модуль для подписки на каналы.\n
    By BENGAL & @pavlyxa_rezon"""

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "subscribed_channel_id",
                2035849227,
                "ID привязанного канала для подписки",
                validator=loader.validators.Integer()
            ),
        )

    def extract_channel_from_link(self, text):
        # Извлечение имени канала из ссылки https://t.me/username
        reg = re.compile(r"https://t.me/([^/]+)")
        match = reg.search(text)
        return match.group(1) if match else None

    @loader.watcher(only_channels=True)
    async def subscribe_to_channel(self, message):
        chat = utils.get_chat_id(message)
        if chat == self.config["subscribed_channel_id"]:
            channel = self.extract_channel_from_link(message.text)
            if channel:
                try:
                    await message.client(functions.channels.JoinChannelRequest(channel))
                except Exception as e:
                    logger.error(f"Ошибка при подписке на канал {channel}: {e}")

    def extract_channel_from_link(self, text):
        # Извлечение имени канала из ссылки https://t.me/username
        reg = re.compile(r"https://t.me/([^/]+)")
        match = reg.search(text)
        return match.group(1) if match else None
