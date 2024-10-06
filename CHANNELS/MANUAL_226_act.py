import re
from telethon.tl.types import Message
from .. import loader, utils
from telethon.tl import functions
import asyncio

@loader.tds
class MANUALMod(loader.Module):
    """Модуль управления каналами.
           Commands: /manual @\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {
        "name": "BGL-MANUAL",
        "manual_main": (
            "<b>💻 Модуль: BGL-CHANNELS</b>\n\n"
            "После установки модуля вам нужно выполнить несколько простых действий для раскрытия полного функционала модуля. "
            "Без настройки он тоже будет работать, если что.\n\n"
        ),
        "manual_basic": (
            "Для начала нужно разделить все ваши аккаунты на условные группы (по умолчанию стоит группа 1). "
            "Для упрощения ставим как на сервере (по 15-20 аккаунтов). "
            "Это создает задержку между выполнениями действий каждой группы в Х*20 секунд.\n\n"
            "Далее на одном из аккаунтов каждой группы нужно включить логгирование (по умолчанию оно выключено). "
            "Так логи будут выводиться только с выбранных аккаунтов прямо в вашу группу.\n"
        ),
        "manual_config": (
            "<b>🔗 Конфигурация:</b>\n"
            "CMD: /reconf [name] [value] [acc]\n\n"
            "<b>Параметры и их аргументы\n</b>"
            "—logger — булевый статус (True/False, 1/0, yes/no).\n"
            "—group — номер сервера или группы аккаунтов.\n"
            "—acc — один или несколько юзеров, где нужно перезаписать конфиг (all для всех).\n"
        ),
        "manual_subscr": (
            "<b>🔗 Подписки: /sub [target]</b>\n"
            "PUBLIC: https://t.me/, t.me/ или @\n"
            "PRIVATE: https://t.me/+, t.me/+\n"
        ),
        "manual_unsubs": (
            "<b>🔗 Отписки: /uns [target]</b>\n"
            "PUBLIC: https://t.me/, //t.me/ или @\n"
            "PRIVATE: ID в формате 100... (без минуса).\n"
        ),
        "back": "Назад"
    }
    
    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643

    @loader.unrestricted
    async def send_manual_message(self):
        """Обработка команды /manual"""
        image_url = "https://raw.githubusercontent.com/BENGALX/SOFT/bengal/IMAGE/BENGAL.jpg"
        await self.inline.form(
            self.owner_chat,
            text=self.strings["manual_main"],
            message=None,
            image=image_url,
            reply_markup=
            [
                [
                    {"text": "Readme", "callback": self.inline__manual_basic},
                    {"text": "Config", "callback": self.inline__manual_config}
                ],
                [
                    {"text": "Subscribe", "callback": self.inline__manual_subscr},
                    {"text": "UnSubscr", "callback": self.inline__manual_unsubs}
                ],
            ],
        )

    @loader.inline_callback("manual_basic")
    async def inline__manual_basic(self, call):
        await call.edit(
            text=self.strings["manual_basic"],
            reply_markup=[[{"text": self.strings["back"], "callback": self.inline__back}]],
        )
        
    @loader.inline_callback("manual_config")
    async def inline__manual_config(self, call):
        await call.edit(
            text=self.strings["manual_config"],
            reply_markup=[
                [
                    {"text": self.strings["back"], "callback": self.inline__back}
                ]
            ],
        )

    @loader.inline_callback("manual_subscr")
    async def inline__manual_subscr(self, call):
        await call.edit(
            text=self.strings["manual_subscr"],
            reply_markup=[
                [
                    {"text": self.strings["back"], "callback": self.inline__back}
                ]
            ],
        )

    @loader.inline_callback("manual_subscr")
    async def inline__manual_unsubs(self, call):
        await call.edit(
            text=self.strings["manual_unsubs"],
            reply_markup=[
                [
                    {"text": self.strings["back"], "callback": self.inline__back}
                ]
            ],
        )

    @loader.inline_callback("manual_main")
    async def inline__back(self, call):
        await call.edit(
            text=self.strings["manual_main"],
            reply_markup=
            [
                    [
                        {"text": "Readme", "callback": self.inline__manual_basic},
                        {"text": "Config", "callback": self.inline__manual_config}
                    ],
                    [
                        {"text": "Subscribe", "callback": self.inline__manual_subscr},
                        {"text": "UnSubscr", "callback": self.inline__manual_unsubs}
                    ],
                ],
        )

    async def handle_manual(self, text):
        """Обработка команды /manual"""
        parts = text.split()
        if len(parts) < 2:
            return

        user = await self.client.get_me()
        if parts[1] == f"@{user.username}":
            await self.send_manual_message()
        else:
            return
    
    @loader.watcher()
    async def watcher_group(self, message):
        """Handle commands calling"""
        if message.chat_id != self.owner_chat:
            return
        if message.sender_id not in self.owner_list:
            return
        try:
            if message.message.startswith("/manual"):
                await self.handle_manual(message.message)
        except:
            pass
