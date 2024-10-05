import re
from telethon.tl import functions
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest

import asyncio
from .. import loader

@loader.tds
class CHANNELSMod(loader.Module):
    """Модуль управления каналами.
           Commands: /manual @\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {"name": "BGL-CHANNELS"}
    
    def __init__(self):
        self.owner_list = [922318957, 1868227136]
        self.moder = 922318957
        self.owner_chat = -1002205010643
        
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "logger", False, "Статус работы логгера (0/1).",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "group", 1, "Номер хоста или группы.",
                validator=loader.validators.Integer(),
            )
    )

    
    def get_delay_host(self):
        """Значение задержки"""
        delay_seconds = self.config["group"] * 20
        return delay_seconds
        
    async def delay_host(self):
        """Задержка выполняется"""
        delay_seconds = self.get_delay_host()
        await asyncio.sleep(delay_seconds)
        return delay_seconds
        

    async def send_module_message(self, text, delay_info=None):
        """Логи действий модуля"""
        if not self.config["logger"]:
            return
        if not self.owner_chat:
            return
        try:
            delay_text = f", Delay: {delay_info} сек" if delay_info else ", Delay: 0."
            logger_message = f"💻 <b>Server: {self.config['group']}{delay_text}</b>\n\n{text}"
            await self.client.send_message(self.owner_chat, logger_message, link_preview=False)
        except:
            pass

    async def send_config_message(self, text):
        """Логи изменений конфигураторов"""
        if not self.owner_chat:
            return
        logger_message = f"💻 <b>Server: {self.config['group']}: </b>{text}"
        await self.client.send_message(self.owner_chat, logger_message)
        
    async def send_manual_message(self, text):
        """Обработка команды /manual"""
        parts = text.split()
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
            await self.client.send_file(self.owner_chat, image_url, caption=manual_part1)
            await asyncio.sleep(2)
            await self.client.send_message(self.owner_chat, manual_part2)
            await asyncio.sleep(2)
            await self.client.send_message(self.owner_chat, manual_part3)
            
    
    async def subscribe_public(self, target):
        """Подписывается на публичные."""
        done_message = f"<b>✅ SUBSCRIBE (Public):</b> {target}"
        fail_message = f"<b>🚫 SUB ERROR (Public):</b> "
        try:
            await self.client(JoinChannelRequest(channel=target))
            await self.send_module_message(done_message, delay_info=self.get_delay_host())
        except Exception as e:
            await self.send_module_message(f"{fail_message}\n{e}")

    async def subscribe_private(self, target):
        """Подписывается на частные."""
        done_message = f"<b>✅ SUBSCRIBE (Private):</b> {target}"
        fail_message = f"<b>🚫 SUB ERROR (Private):</b> "
        try:
            invite_hash = target.split("t.me/+")[1]
            await self.client(ImportChatInviteRequest(invite_hash))
            await self.send_module_message(done_message, delay_info=self.get_delay_host())
        except Exception as e:
            await self.send_module_message(f"{fail_message}\n{e}")

    
    async def unsubscribe_by_tag(self, target):
        """Отписка по юзернейму."""
        done_message = f"<b>✅ UNSUBSCRIBE:</b> {target}"
        user_message = f"<b>✅ DELETE:</b> {target}"
        try:
            await self.client(functions.channels.LeaveChannelRequest(target))
            await self.send_module_message(done_message, delay_info=self.get_delay_host())
        except:
            await self.client.delete_dialog(target)
            await self.send_module_message(user_message, delay_info=self.get_delay_host())

    async def unsubscribe_by_link(self, target):
        """Отписка по обычной ссылке."""
        match = re.search(r't\.me/([a-zA-Z0-9_]+)', target)
        done_message = f"<b>✅ UNSUBSCRIBE:</b>\n{target}"
        user_message = f"<b>✅ DELETE:</b>\n{target}"
        if match:
            username = match.group(1)
            try:
                await self.client(functions.channels.LeaveChannelRequest(username))
                await self.send_module_message(done_message, delay_info=self.get_delay_host())
            except:
                await self.client.delete_dialog(username)
                await self.send_module_message(user_message, delay_info=self.get_delay_host())
        else:
            await self.send_module_message("🚫 UNSUBSCRIBE error")

    async def unsubscribe_by_id(self, target):
        """Отписка по айди."""
        done_message = f"<b>✅ UNSUBSCRIBE ID:</b> {target}"
        user_message = f"<b>✅ DELETE ID:</b> {target}"
        try:
            channel_id = int(target)
            await self.client(functions.channels.LeaveChannelRequest(channel_id))
            await self.send_module_message(done_message, delay_info=self.get_delay_host())
        except:
            await self.client.delete_dialog(channel_id)
            await self.send_module_message(user_message, delay_info=self.get_delay_host())
            

    async def update_user_config(self, config_name, new_value):
        """Обновление конфиг параметров."""
        if config_name not in self.config:
            return
        else:
            if isinstance(self.config[config_name], bool):
                new_value = new_value.lower() in ['true', '1', 'yes']
            elif isinstance(self.config[config_name], int):
                new_value = int(new_value)
            self.config[config_name] = new_value
            done_message = f"<b>✅ CONFIG:\nПараметр {config_name} изменен на {new_value}.</b>"
            await self.send_config_message(done_message)
            

    async def handle_subscribe(self, text):
        """Центральная обработка /sub"""
        target = text.split("/sub", 1)[1].strip()
        await self.delay_host()
        if 't.me/+' in target:
            await self.subscribe_private(target)
        elif "t.me/" in target or "@" in target:
            await self.subscribe_public(target)
        else:
            await self.send_module_message("<b>🚫 SUBSCRIBE ERROR:</b> Неверный формат.")

    async def handle_unsubscribe(self, text):
        """Центральная обработка /uns"""
        target = text.split("/uns", 1)[1].strip()
        await self.delay_host()
        if target.startswith("@"):
            await self.unsubscribe_by_tag(target)
        elif "t.me/" in target:
            await self.unsubscribe_by_link(target)
        elif target.isdigit():
            await self.unsubscribe_by_id(target)
        else:
            await self.send_module_message("<b>🚫 UNSUBSCRIBE ERROR:</b> Неверный формат.")

    async def handle_user_config(self, text):
        """USER configuration of module"""
        parts = text.split()
        if len(parts) < 4:
            return
        config_name = parts[1]
        new_value = parts[2]
        taglist = parts[3:]
        user = await self.client.get_me()
        if "all" in taglist:
            await self.update_user_config(config_name, new_value)
        else:
            for tag in taglist:
                if tag == f"@{user.username}":
                    await self.update_user_config(config_name, new_value)
    
    @loader.watcher()
    async def watcher_group(self, message):
        """Handle commands calling"""
        if message.chat_id != self.owner_chat:
            return
        if message.sender_id not in self.owner_list:
            return
            
        try:
            if message.message.startswith("/sub"):
                await self.handle_subscribe(message.message)
            elif message.message.startswith("/uns"):
                await self.handle_unsubscribe(message.message)
            
            elif message.message.startswith("/reconf"):
                await self.handle_user_config(message.message)
            elif message.message.startswith("/manual"):
                await self.send_manual_message(message.message)
        except:
            pass
