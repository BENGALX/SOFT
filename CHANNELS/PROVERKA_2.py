import logging
from telethon.tl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class InlineVizitkaMod(loader.Module):
    strings = {
        "name": "InlineVizitka",
        "main_text": "<b>Выберите вариант:</b>",
        "choice_1": "<b>Вы ввели 1</b>",
        "choice_2": "<b>Вы ввели 2</b>",
        "back": "Назад",
    }

    strings_ru = {
        "main_text": "<b>Выберите вариант:</b>",
        "choice_1": "<b>Вы ввели 1</b>",
        "choice_2": "<b>Вы ввели 2</b>",
        "back": "Назад",
    }

    @loader.unrestricted
    async def visitkacmd(self, message: Message):
        """Отображает визитку с выбором"""
        await self.inline.form(
            message=message,
            text=self.strings("main_text"),
            reply_markup=[
                [
                    {"text": "1", "switch_inline": "1"},
                    {"text": "2", "switch_inline": "2"},
                ],
            ],
        )

    async def inline_handler(self, query):
        choice = query.query
        if choice == "1":
            await query.edit(
                text=self.strings("choice_1"),
                reply_markup=[[{"text": self.strings("back"), "switch_inline": ""}]],
            )
        elif choice == "2":
            await query.edit(
                text=self.strings("choice_2"),
                reply_markup=[[{"text": self.strings("back"), "switch_inline": ""}]],
            )
