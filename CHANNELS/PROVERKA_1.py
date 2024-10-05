import logging
from telethon.tl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class InlineVizitkaMod(loader.Module):
    strings = {
        "name": "InlineVizitka",
        "mysocial": "<b>✨ My social networks</b>",
        "userules": (
            "<b>How this module is used</b>\n1. Links to social networks must be"
            " entered in <code>{prefix}config</code>\n2. Links in the config must start"
            " with https:// otherwise there will be an <b>error</b>"
        ),
    }

    strings_ru = {
        "mysocial": "<b>✨ Мои соцсети</b>",
        "userules": (
            "<b>Как пользоваться данным модулем</b>\n1. Ссылки на соц.сети надо вводить"
            " в <code>{prefix}config</code>\n2. Ссылки в конфиге должны начинаться с"
            " https:// иначе будет <b>ошибка</b>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "discord",
                "🚫 Link not set",
                lambda: "You discord LINK",
            ),
            loader.ConfigValue(
                "twitter",
                "🚫 Link not set",
                lambda: "You twitter LINK",
            ),
        )

    @loader.unrestricted
    async def vizitkacmd(self, message: Message):
        """Command for displaying a business card"""
        await self.inline.form(
            message=message,
            text=self.config["custom_message"] or "<b>✨ Мои соцсети</b>",
            reply_markup=[
                [
                    {"text": "🥱 Discord", "callback": self.inline__callAnswer},
                    {"text": "🌐 Twitter", "url": self.config["twitter"]},
                ],
            ],
        )

    async def inline__callAnswer(self, call):
        await call.answer(self.config["discord"], show_alert=True)

    async def vizinfocmd(self, message: Message):
        await utils.answer(
            message,
            self.strings("userules").format(prefix=self.get_prefix()),
        )
