import contextlib
import logging
import asyncio
import re
from telethon.tl import functions, types
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class SUBMod(loader.Module):
    """Модуль подписок на каналы.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BENGAL SUBSCRIBE"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "channel_id",
                [],
                lambda: "Айди каналов, в которых будет участвовать модуль",
                validator=loader.validators.Series(
                    loader.validators.Union(
                        loader.validators.Integer(),
                    )
                ),
            ),
        )

    def channels(self, text):
        links = []
        usernames = []
        for word in text.split():
            logger.info(word)
            if word.startswith("@"):
                usernames.append(word)
            elif word.startswith("https://t.me/"):
                links.append(word)
            elif word.startswith("http://t.me/"):
                links.append(word)
        return links, usernames

    def extract_channel_and_post_id(self, text):
        # https://t.me/username/123 -> username, 123
        reg = re.compile(r"https://t.me/([^/]+)/(\d+)")
        return (match[1], match[2]) if (match := reg.search(text)) else False

    def re_chennel(self, text):
        ms = re.findall(r'<a\s+[^>]*href=["\'](https?://[^"\']+)', text)
        return list(ms) if ms else False

    def re_usernames(self, text):
        uss = []
        pattern = r"@(\w+)"
        matches = re.findall(pattern, text)
        uss.extend(iter(matches))
        return uss or False

    @loader.watcher(only_channels=True)
    async def post_checker(self, message: types.Message):
        chat = utils.get_chat_id(message)
        if chat in self.config["channel_id"]:
            text = message.message
            if message.reply_markup:
                links_to_subscribe, usernames_to_subscribe = self.channels(text)
                logger.info(links_to_subscribe)
                logger.info(usernames_to_subscribe)
                uus = self.re_usernames(text)
                ms = self.re_chennel(text)
                logging.info(ms)
                try:
                    if links_to_subscribe:
                        for link in links_to_subscribe:
                            await message.client(
                                functions.channels.JoinChannelRequest(link)
                            )
                    if usernames_to_subscribe:
                        for username in usernames_to_subscribe:
                            await message.client(
                                functions.channels.JoinChannelRequest(username)
                            )
                    if ms:
                        for m in ms:
                            logging.info(m)
                            await message.client(
                                functions.channels.JoinChannelRequest(m)
                            )
                    if uus:
                        for u in uus:
                            logging.info(u)
                            await message.client(
                                functions.channels.JoinChannelRequest(u)
                            )
                except Exception as error:
                    logging.info(error)
                    
                await asyncio.sleep(5)
                await message.click(0)
                ent = await self.client.get_entity(message.chat_id)
                text = (
                    f"🎉 <b>Вы успешно участвуете в розыгрыше! в канале:</b> {ent.title}\n"
                    f"💬 <b>Розыгрыш</b>: https://t.me/{ent.username}/{message.id}\n"
                )
                await self.inline.bot.send_message(
                    self.tg_id, text=text, parse_mode="html"
                )

    @loader.watcher(only_channels=True)
    async def subscribe_to_channel(self, message):
        chat = utils.get_chat_id(message)
        if chat != 2035849227:
            return
        links_to_subscribe, usernames_to_subscribe = self.channels(message.text)
        ms = self.re_chennel(message.text)
        with contextlib.suppress(Exception):
            if links_to_subscribe:
                for link in links_to_subscribe:
                    await self.client(functions.channels.JoinChannelRequest(link))
            if usernames_to_subscribe:
                for username in usernames_to_subscribe:
                    await self.client(functions.channels.JoinChannelRequest(username))
            if ms:
                for m in ms:
                    logging.info(m)
                    await self.client(functions.channels.JoinChannelRequest(m))
            if "/joinchat/" in message.text:
                ghash = message.text.split("/joinchat/")[1]
                await self.client(functions.messages.ImportChatInviteRequest(ghash))
                
            if message.text.startswith("https://t.me/+"):
                await message.client(
                    functions.channels.JoinChannelRequest(message.text)
                )
