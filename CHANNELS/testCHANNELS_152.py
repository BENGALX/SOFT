import asyncio
from .. import loader

@loader.tds
class CHANNELSManualMod(loader.Module):
    """Модуль для вывода мануала с инлайн-кнопками.
       ⚙️ By @pavlyxa_rezon"""

    strings = {"name": "BGL-CHANNELS-Manual"}

    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643

    async def send_manual_message(self, message, mode="main"):
        """Отправка сообщения с инлайн-кнопками, изменяемыми при нажатии"""
        manual_main = (
            f"<b>💻 Модуль: BGL-CHANNELS-Manual</b>\n\n"
            f"<b>🔗 Основная информация:</b>\n"
            f"Это основное сообщение мануала. Нажмите на кнопки ниже для получения детальной информации."
        )

        manual_config = (
            f"<b>🔗 Конфигурация:</b>\n"
            f"— group — номер сервера или группы.\n"
            f"Используйте /reconf для изменения значений.\n"
        )

        manual_subs = (
            f"<b>🔗 Функции подписок и отписок:</b>\n"
            f"Здесь вы можете управлять подписками и отписками (потенциальная функциональность модуля).\n"
        )

        if mode == "main":
            text = manual_main
            buttons = [
                [{"text": "⚙️ Конфигурация", "callback": self.inline__show_config}],
                [{"text": "📜 Подписки/Отписки", "callback": self.inline__show_subs}],
            ]
        elif mode == "config":
            text = manual_config
            buttons = [
                [{"text": "🔙 Назад", "callback": self.inline__show_main}],
            ]
        elif mode == "subs":
            text = manual_subs
            buttons = [
                [{"text": "🔙 Назад", "callback": self.inline__show_main}],
            ]

        await self.inline.form(
            message=message,
            text=text,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )

    async def watcher_group(self, message):
        """Обработка команд только от владельцев и в привязке к чату"""
        if message.chat_id != self.owner_chat:
            return
        if message.sender_id not in self.owner_list:
            return

        try:
            if message.message.startswith("/manual"):
                parts = message.message.split()
                if len(parts) >= 2:
                    user = await self.client.get_me()
                    if parts[1] == f"@{user.username}":
                        await self.send_manual_message(message, mode="main")
        except:
            pass

    async def inline__show_main(self, call):
        """Показать основное сообщение"""
        await self.send_manual_message(call, mode="main")

    async def inline__show_config(self, call):
        """Показать информацию о конфигурации"""
        await self.send_manual_message(call, mode="config")

    async def inline__show_subs(self, call):
        """Показать информацию о подписках и отписках"""
        await self.send_manual_message(call, mode="subs")
