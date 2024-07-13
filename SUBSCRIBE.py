import logging
import re
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import PeerChannel, PeerChat
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class SUBMod(loader.Module):
    """Модуль подписок на каналы.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL_SUBSCR"}
    
    async def send_bot_message(self, text):
        await self.client.send_message('me', text, link_preview=False)

    @loader.watcher()
    async def watcher(self, message):
        chat_id = 2035849227
        try:
            if isinstance(message.peer_id, (PeerChannel, PeerChat)) and message.peer_id.channel_id == chat_id:
                if "t.me/" in message.message:
                    links = re.findall(r'https?://t.me/.*', message.message)
                    for link in links:
                        success_message = f"<b>Вы успешно подписались на канал:</b>\n {link}"
                        try:
                            await self.client(JoinChannelRequest(channel=link))
                            await self.send_bot_message(success_message)
                        except Exception as e:
                            logger.error(f"Error joining channel: {e}")
                            try:
                                invite_hash = link.split("t.me/+")[1]
                                await self.client(ImportChatInviteRequest(invite_hash))
                                await self.send_bot_message(success_message)
                            except Exception as e:
                                logger.error(f"Error importing chat invite: {e}")
        except Exception as e:
            logger.error(f"Error in watcher: {e}")
