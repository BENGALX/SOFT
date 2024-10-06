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

    strings = {"name": "BGL-MANUAL"}
    
    def __init__(self):
        self.owner_list = [922318957, 1868227136]
        self.owner_chat = -1002205010643

    @loader.unrestricted
    async def send_manual_message(self, text):
        """Обработка команды /manual"""
        parts = text.split()
        if len(parts) < 2:
            return
        
        manual_main = (
            f"<b>💻 Модуль: BGL-CHANNELS</b>\n\n"
            f"После установки модуля вам нужно выполнить несколько простых действий для раскрытия полного функционаа модуля. "
            f"Без настройки он тоже будет работат если что.\n\n"
        )

        manual_basic = (
            f"Для начала нужно разделить все ваши аккаунты на условные группы (по умолчанию стоит группа 1). "
            f"Для упрощения ставим как на сервере (по 15-20 аккаунтов). "
            f"Это создает задержку между выполнениями действий каждой группы в Х*20 секунд.\n\n"
            f"Далее на одном из аккаунтов каждой группы нужно включить логгирование (по умолчанию оно выключено). "
            f"Так логи будут выводиться только с выбранных аккаунтов прямо в вашу группу.\n"
        )

        manual_config = (
            f"<b>🔗 Конфигурация:</b>\n"
            f"CMD: /reconf [name] [value] [acc]\n\n"
            f"<b>Параметры и их аргументы\n</b>"
            f"—logger — булевый статус (True/False, 1/0, yes/no).\n"
            f"—group — номер сервера или группы аккаунтов.\n"
            f"—acc — один или несколько юзеров, где нужно перезаписать конфиг (all для всех).\n"
        )

        manual_subscr = (
            f"<b>🔗 Подписки: /sub [target]</b>\n"
            f"PUBLIC: https://t.me/, t.me/ или @\n"
            f"PRIVATE: https://t.me/+, t.me/+\n"
        )

        manual_unsubs = (
            f"<b>\n🔗 Отписки: /uns [target]</b>\n"
            f"PUBLIC: https://t.me/, //t.me/ или @\n"
            f"PRIVATE: ID в формате 100... (без минуса).\n"
        )

        image_url = "https://raw.githubusercontent.com/BENGALX/SOFT/bengal/IMAGE/BENGAL.jpg"
        user = await self.client.get_me()
        if parts[1] == f"@{user.username}":
            await self.inline.form(
                self.owner_chat, image_url,
                message=message,
                text=self.strings("manual_main"),
                reply_markup=[
                    [{"text": "1", "callback": self.inline__choice_1}, {"text": "2", "callback": self.inline__choice_2}],
                ],
            )
            
    async def inline__manual_basic(self, call):
        await call.edit(
            text=self.strings("manual_basic"),
            reply_markup=[[{"text": self.strings("back"), "callback": self.inline__back}]],
        )

    async def inline__manual_config(self, call):
        await call.edit(
            text=self.strings("manual_config"),
            reply_markup=[[{"text": self.strings("back"), "callback": self.inline__back}]],
        )

    async def inline__manual_subscr(self, call):
        await call.edit(
            text=self.strings("manual_subscr"),
            reply_markup=[[{"text": self.strings("back"), "callback": self.inline__back}]],
        )

    async def inline__manual_unsubs(self, call):
        await call.edit(
            text=self.strings("manual_unsubs"),
            reply_markup=[[{"text": self.strings("back"), "callback": self.inline__back}]],
        )

    async def inline__back(self, call):
        await call.edit(
            text=self.strings("manual_main"),
            reply_markup=[
                [{"text": "1", "callback": self.inline__choice_1}, {"text": "2", "callback": self.inline__choice_2}],
            ],
        )
    
    @loader.watcher()
    async def watcher_group(self, message):
        """Handle commands calling"""
        if message.chat_id != self.owner_chat:
            return
        if message.sender_id not in self.owner_list:
            return
        try:
            elif message.message.startswith("/manual"):
                await self.send_manual_message(message.message)
        except:
            pass
