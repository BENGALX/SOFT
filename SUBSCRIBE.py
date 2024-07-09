import logging
from telethon.tl import functions
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ChannelSubscribeMod(loader.Module):
    """Модуль для подписки на каналы"""

    @loader.watcher(only_in_chat=True, chats=[2035849227])
    async def subscribe_to_channel(self, message):
        text = message.text.strip()
        if text.startswith("https://t.me/") and not text.startswith("https://t.me/+"):
            try:
                await message.client(functions.channels.JoinChannelRequest(text))
            except Exception as e:
                logger.error(f"Failed to join channel {text}: {e}")

        elif "/joinchat/" in text:
            ghash = text.split("/joinchat/")[1]
            try:
                await message.client(functions.messages.ImportChatInviteRequest(ghash))
            except Exception as e:
                logger.error(f"Failed to join chat invite {ghash}: {e}")

    @loader.watcher(only_in_chat=True, chats=[2035849227])
    async def unsubscribe_channel(self, message):
        text = message.text.strip()
        if text.startswith("https://t.me/") and not text.startswith("https://t.me/+"):
            try:
                await message.client(functions.channels.LeaveChannelRequest(text))
            except Exception as e:
                logger.error(f"Failed to leave channel {text}: {e}")

    async def client_ready(self, client, db):
        self.client = client
