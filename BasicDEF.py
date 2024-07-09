import contextlib
import logging
import asyncio
import re
from telethon.tl import functions, types
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class RaffleMod(loader.Module):
    """Модуль рафлер деф.\n
    By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL DEF"}

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
    async def get_and_subscribe(self, message: types.Message):
        """
        This watcher will take the link to post and get the message and do the raffle
        """
        chat = message.chat_id
        if chat != -1002035849227:
            return
        em = message.text
        logger.info(em)
        channel, _id = self.extract_channel_and_post_id(em)
        uss = self.re_usernames(em)
        if not channel or not _id:
            return logger.info("No channel or post id")
        logger.info(channel)
        logger.info(_id)
        post = (await self.client.get_messages(channel, ids=[int(_id)]))[0]
        if post.reply_markup:
            links_to_subscribe, usernames_to_subscribe = self.channels(post.text)
            logger.info(links_to_subscribe)
            logger.info(usernames_to_subscribe)
            ms = self.re_chennel(post.text)
            try:
                if links_to_subscribe:
                    for link in links_to_subscribe:
                        await self.client(functions.channels.JoinChannelRequest(link))
                if usernames_to_subscribe:
                    for username in usernames_to_subscribe:
                        await self.client(
                            functions.channels.JoinChannelRequest(username)
                        )
                if ms:
                    for m in ms:
                        logging.info(m)
                        await self.client(functions.channels.JoinChannelRequest(m))
                if uss:
                    for u in uss:
                        logging.info(u)
                        await self.client(functions.channels.JoinChannelRequest(u))
            except Exception as e:
                logger.info(e)
            logger.info("clicking")
        huy = await post.click(0)
        logger.info(huy)
        await asyncio.sleep(5)
        ent = await self.client.get_entity(post.chat_id)
        text = (
            f"🎉 <b>Вы успешно участвуете в розыгрыше! в канале:</b> {ent.title}\n"
            f"💬 <b>Розыгрыш</b>: https://t.me/{ent.username}/{post.id}\n"
        )
        S = await post.click(0)
        await post.click(0)
        logger.info(S)
        await self.inline.bot.send_message(self.tg_id, text=text, parse_mode="html")

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

    @loader.watcher(only_channels=True)
    async def unsubscribe_channel(self, message):
        chat = message.chat_id
        if chat != -1002035849227:
            return
        try:
            await self.client(functions.channels.LeaveChannelRequest(message.text))
        except Exception as e:
            await self.client.delete_dialog(message.text)
        else:
            logger.info("Unsubscribed from channel")
