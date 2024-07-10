import asyncio
import logging
import re
from .. import loader, utils
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

logger = logging.getLogger(__name__)

@loader.tds
class SUBMod(loader.Module):
    """Модуль подписок на каналы.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_SUBSCR"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chat_id", 2035849227, "ID",
                validator=loader.validators.Integer(),
            )
        )

    async def send_subscribe_message(self, chat_id, channel_name):
        text = f"<b>Вы успешно подписались на {channel_name}</b>"
        logger.info(f"Отправка сообщения: {text} в чат {chat_id}")
        await self.inline.bot.send_message(chat_id, text=text, parse_mode="html")

    @loader.watcher()
    async def watcher(self, message):
        logger.info(f"Получено сообщение: {message.message} от {message.peer_id}")
        try:
            if hasattr(message.peer_id, 'channel_id') and message.peer_id.channel_id == self.config["chat_id"]:
                logger.info(f"Сообщение из канала с ID: {self.config['chat_id']}")
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    for link in links:
                        logger.info(f"Найдена ссылка: {link}")
                        try:
                            await self._client(JoinChannelRequest(channel=link))
                            await self.send_subscribe_message(self.config["chat_id"], link)
                        except Exception as e:
                            invite_code = link.split("t.me/+")[-1]
                            logger.info(f"Попытка подписки через ImportChatInviteRequest: {invite_code}")
                            await self._client(ImportChatInviteRequest(invite_code))
                            await self.send_subscribe_message(self.config["chat_id"], link)
                            logger.error(f"Ошибка при подписке через JoinChannelRequest: {e}")
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения из канала: {e}")

        try:
            if hasattr(message.peer_id, 'chat_id') and message.peer_id.chat_id == self.config["chat_id"]:
                logger.info(f"Сообщение из чата с ID: {self.config['chat_id']}")
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    for link in links:
                        logger.info(f"Найдена ссылка: {link}")
                        try:
                            await self._client(JoinChannelRequest(channel=link))
                            await self.send_subscribe_message(self.config["chat_id"], link)
                        except Exception as e:
                            invite_code = link.split("t.me/+")[-1]
                            logger.info(f"Попытка подписки через ImportChatInviteRequest: {invite_code}")
                            await self._client(ImportChatInviteRequest(invite_code))
                            await self.send_subscribe_message(self.config["chat_id"], link)
                            logger.error(f"Ошибка при подписке через JoinChannelRequest: {e}")
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения из чата: {e}")
