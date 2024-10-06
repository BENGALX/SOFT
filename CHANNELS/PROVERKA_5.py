import logging
from telethon.tl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class InlineVizitkaMod(loader.Module):
    strings = {
        "name": "InlineVizitka",
        "main_text": "<b>Выберите вариант:</b>",
        "choice_1": "<b>Вы выбрали 1</b>",
        "choice_2": "<b>Вы выбрали 2</b>",
        "back": "Назад",
    }

    @loader.unrestricted
    async def visitkacmd(self, message: Message):
        """Отображает визитку с выбором"""
        await self.inline.form(
            message=message,
            text=self.strings("main_text"),
            reply_markup=[
                [{"text": "1", "callback": self.inline__choice_1}],
                [{"text": "2", "callback": self.inline__choice_2}],
            ],
        )

    async def inline__choice_1(self, call):
        await call.edit(
            text=self.strings("choice_1"),
            reply_markup=[[{"text": self.strings("back"), "callback": self.inline__back}]],
        )

    async def inline__choice_2(self, call):
        await call.edit(
            text=self.strings("choice_2"),
            reply_markup=[[{"text": self.strings("back"), "callback": self.inline__back}]],
        )

    async def inline__back(self, call):
        await call.edit(
            text=self.strings("main_text"),
            reply_markup=[
                [{"text": "1", "callback": self.inline__choice_1}],
                [{"text": "2", "callback": self.inline__choice_2}],
            ],
        )
