import re
from telethon.tl import functions
import asyncio
from .. import loader

@loader.tds
class CHANNELSMod(loader.Module):
    """Модуль управления каналами.
           Commands: /manual @\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {"name": "BGL-CHANNELS"}
    
    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643

    async def send_manual_message(self, message, mode="main"):
        """Обработка команды /manual"""
        parts = message.message.split()
        if len(parts) < 2:
            return
        
        manual_part1 = (
            f"<b>💻 Модуль: BGL-CHANNELS</b>\n\n"
            f"<b>🔗 Справка:</b> /manual @user\n\n"
            f"<b>🔗 Базовая настройка.</b>\n"
            f"После установки модуля вам нужно выполнить несколько простых действий для раскрытия полного функционаа модуля. "
            f"Без настройки он тоже будет работат если что.\n\n"
            f"Для начала нужно разделить все ваши аккаунты на условные группы (по умолчанию стоит группа 1). "
            f"Для упрощения ставим как на сервере (по 15-20 аккаунтов). "
            f"Это создает задержку между выполнениями действий каждой группы в Х*20 секунд.\n\n"
            f"Далее на одном из аккаунтов каждой группы нужно включить логгирование (по умолчанию оно выключено). "
            f"Так логи будут выводиться только с выбранных аккаунтов прямо в вашу группу.\n"
        )

        manual_part2 = (
            f"<b>🔗 Конфигурация:</b>\n"
            f"CMD: /reconf [name] [value] [acc]\n\n"
            f"<b>Параметры и их аргументы\n</b>"
            f"—logger — булевый статус (True/False, 1/0, yes/no).\n"
            f"—group — номер сервера или группы аккаунтов.\n"
            f"—acc — один или несколько юзеров, где нужно перезаписать конфиг (all для всех).\n"
        )

        manual_part3 = (    
            f"Текущий функционал модуля:\n\n"
            f"<b>🔗 1. Подписки: /sub [target]</b>\n"
            f"PUBLIC: https://t.me/, t.me/ или @\n"
            f"PRIVATE: https://t.me/+, t.me/+\n"
    
            f"<b>\n🔗 2. Отписки: /uns [target]</b>\n"
            f"PUBLIC: https://t.me/, //t.me/ или @\n"
            f"PRIVATE: ID в формате 100... (без минуса).\n"
        )

        image_url = "https://raw.githubusercontent.com/BENGALX/SOFT/bengal/IMAGE/BENGAL.jpg"
        user = await self.client.get_me()
        if parts[1] == f"@{user.username}":
            if mode == "main":
                text = manual_part1
                buttons = [
                    [{"text": "⚙️ Конфигурация", "callback": self.inline__show_config}],
                    [{"text": "📜 Функции", "callback": self.inline__show_functions}],
                ]
            elif mode == "config":
                text = manual_part2
                buttons = [
                    [{"text": "🔙 Назад", "callback": self.inline__show_main}],
                ]
            elif mode == "functions":
                text = manual_part3
                buttons = [
                    [{"text": "🔙 Назад", "callback": self.inline__show_main}],
                ]
                
            await self.inline.form(
                message=message,
                text=text,
                reply_markup=buttons,
                disable_web_page_preview=True,
                file=image_url if mode == "main" else None
            )
            
    @loader.watcher()
    async def watcher_group(self, message):
        """Handle commands calling"""
        if message.chat_id != self.owner_chat:
            return
        if message.sender_id not in self.owner_list:
            return
            
        try:
            if message.message.startswith("/manual"):
                await self.send_manual_message(message, mode="main")
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    async def inline__show_main(self, call):
        """Показать основное сообщение"""
        await self.send_manual_message(call, mode="main")

    async def inline__show_config(self, call):
        """Показать информацию о конфигурации"""
        await self.send_manual_message(call, mode="config")

    async def inline__show_functions(self, call):
        """Показать информацию о функциях"""
        await self.send_manual_message(call, mode="functions")
