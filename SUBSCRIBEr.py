import re
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import asyncio
from .. import loader

@loader.tds
class SUBMod(loader.Module):го
    """Модуль подписок на каналы.
           Commands: /helpsub @\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {"name": "BGL-SUBSCRIBE"}
    
    def __init__(self):
        self.module_enabled = True
        self.owner_list = [922318957, 1804908120]
        self.moder = 922318957
        
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chat_owner_id", -1002156895908, "Группа со вводом активаторов.",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "chat_logs_id", -1002156895908, "Группа с выводом всех логов.",
                validator=loader.validators.Integer(),
            ),
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
        delay_seconds = self.config["group"] * 10
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
        if not self.config["chat_logs_id"]:
            return
        try:
            delay_text = f", Delay: {delay_info} сек" if delay_info else ""
            logger_message = f"💻 <b>Server: {self.config['group']}{delay_text}</b>\n\n{text}"
            await self.client.send_message(self.config["chat_logs_id"], logger_message, link_preview=False)
        except:
            pass

    async def send_config_message(self, text):
        """Логи изменений конфигураторов"""
        if not self.config["chat_logs_id"]:
            return
        logger_message = f"💻 <b>Server: {self.config['group']}: </b>{text}"
        await self.client.send_message(self.config["chat_logs_id"], logger_message)

    async def send_helper_message(self):
        if not self.config["chat_logs_id"]:
            return
        """Справка по модулю"""
        help_text = (f"<b>🔹 Команды модуля:</b>\n\n"
                    f"— /sub [ссылка/username] — Подписаться.\n"
                    f"— /reconf [config] [argument] [@us1 @us2 or all].\n"
                    f"— /helpsub @user — Справка.\n")
        await self.client.send_message(self.config["chat_logs_id"], help_text)
        
    
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

    async def update_user_config(self, config_name, new_value):
        """Обновление конфиг параметров."""
        if config_name in self.config:
            try:
                if isinstance(self.config[config_name], bool):
                    new_value = new_value.lower() in ['true', '1', 'yes']
                elif isinstance(self.config[config_name], int):
                    new_value = int(new_value)
                self.config[config_name] = new_value
                done_message = f"<b>✅ CONFIG:\nПараметр {config_name} изменен на {new_value}.</b>"
                await self.send_config_message(done_message)
            except Exception as e:
                fail_message = f"<b>🚫 CONFIG ERROR:</b>\n{e}"
                await self.send_config_message(fail_message)
        else:
            fail_message = f"<b>🚫 CONFIG ERROR:\n</b>Параметр {config_name} не найден."
            await self.send_config_message(fail_message)

    
    async def handle_helper(self, text):
        """Обработка команды /helpsub"""
        parts = text.split()
        if len(parts) < 2:
            return
        user = await self.client.get_me()
        if parts[1] == f"@{user.username}":
            await self.send_helper_message()

    async def handle_subscribe(self, text):
        """Центральная бработка /sub"""
        target = text.split("/sub", 1)[1].strip()
        if 't.me/+' in target:
            await self.delay_host()
            await self.subscribe_private(target)
        elif "t.me/" in target or "@" in target:
            await self.delay_host()
            await self.subscribe_public(target)
        else:
            await self.send_module_message("<b>🚫 SUBSCRIBE ERROR:</b> Неверный формат.")

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

    async def handle_root_config(self, text, sender_id):
        """ROOT configuration of module"""
        if sender_id != self.moder:
            await self.send_config_message(f"<b>🚫 У вуменов нет прав модера.</b>")
            return
        parts = text.split()
        if len(parts) < 2:
            return 
        if parts[1] in ['true', '1', 'yes']:
            self.module_enabled = True
            await self.send_config_message(f"<b>ROOT:\n✅ MODULE ENABLED.</b>")
        elif parts[1] in ['false', '0', 'no']:
            self.module_enabled = False
            await self.send_config_message(f"<b>ROOT:\n🚫 MODULE DISABLED.</b>")
        else:
            return

    
    @loader.watcher()
    async def watcher_group(self, message):
        """Handle commands calling"""
        if message.chat_id != self.config["chat_owner_id"]:
            return
        if message.message.startswith("root"):
            await self.handle_root_config(message.message, message.sender_id)
        if message.sender_id not in self.owner_list:
            return
            
        try:
            if not self.module_enabled:
                return
            if message.message.startswith("/sub"):
                await self.handle_subscribe(message.message)
            elif message.message.startswith("/reconf"):
                await self.handle_user_config(message.message)
            elif message.message.startswith("/helpsub"):
                await self.handle_helper(message.message)
        except:
            pass