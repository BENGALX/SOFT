import re
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import asyncio
from .. import loader

@loader.tds
class SUBMod(loader.Module):
    """Модуль подписок на каналы.
           Commands: /sub, /reconf\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {"name": "BGL-SUBSCRIBE"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chat_owner_id", -1002187569778, "Группа со вводом активаторов.",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "chat_logs_id", -1002187569778, "Группа с выводом всех логов.",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "logger_enabled", False, "Статус работы логгера (0/1).",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "host_number", 1, "Номер хоста или группы.",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "owner_list", [922318957, 1868227136], "Список допусков к управлению.",
                validator=loader.validators.Series(validator=loader.validators.Integer())
            )
        )

    def get_delay_host(self):
        """Значение задержки (в развитии)"""
        delay_seconds = self.config["host_number"] * 10
        return delay_seconds
        
    async def delay_host(self):
        """Задержка выполняется"""
        delay_seconds = self.get_delay_host()
        await asyncio.sleep(delay_seconds)
        return delay_seconds

    async def send_module_message(self, text, chat_id=None, delay_info=None):
        """Этой шарманкой выводить только логи действий модулей"""
        if not self.config["logger_enabled"]:
            return
        try:
            if chat_id is None:
                chat_id = self.config["chat_logs_id"]
            delay_text = f", Delay: {delay_info} сек" if delay_info else ""
            logger_message = f"💻 <b>Server: {self.config['host_number']}{delay_text}</b>\n\n{text}"
            await self.client.send_message(chat_id, logger_message, link_preview=False)
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")

    async def send_config_message(self, text, chat_id=None):
        """Этой шарманкой выводить только логи изменений конфигураторов"""
        if chat_id is None:
            chat_id = self.config["chat_logs_id"]
        logger_message = f"💻 <b>Server: {self.config['host_number']}: </b>{text}"
        await self.client.send_message(chat_id, logger_message)

    async def subscribe_full(self, target):
        """Подписывается на каналы по ссылке и тегу"""
        done_message = f"<b>✅ SUBSCRIBE:</b> {target}"
        fail_message = f"<b>🚫 SUB ERROR:</b> {target}"
        try:
            await self.client(JoinChannelRequest(channel=target))
            await self.send_module_message(done_message, delay_info=self.get_delay_host())
        except:
            try:
                invite_hash = target.split("t.me/+")[1]
                await self.client(ImportChatInviteRequest(invite_hash))
                await self.send_module_message(done_message, delay_info=self.get_delay_host())
            except Exception as e:
                await self.send_module_message(f"{fail_message}\nОшибка: {e}", delay_info=self.get_delay_host())

    async def update_config(self, config_name, new_value):
        """Метод для обновления конфигурационных параметров."""
        if config_name in self.config:
            try:
                if isinstance(self.config[config_name], bool):
                    new_value = new_value.lower() in ['true', '1', 'yes']
                elif isinstance(self.config[config_name], int):
                    new_value = int(new_value)
                self.config[config_name] = new_value
                done_message = f"<b>✅ CONFIG:\nАргумент {config_name} изменен на {new_value}.</b>"
                await self.send_config_message(done_message)
            except Exception as e:
                fail_message = f"<b>🚫 CONFIG ERROR:</b>\n{e}"
                await self.send_config_message(fail_message)
        else:
            fail_message = f"<b>🚫 CONFIG ERROR:\n</b>Аргумент {config_name} не найден."
            await self.send_config_message(fail_message)

    async def handle_subscribe(self, text):
        """Центральный метод обработки подписок"""
        target = text.split("/sub", 1)[1].strip()
        await self.delay_host()
        await self.subscribe_full(target)

    async def handle_configurator(self, text):
        """Изменение любых конфиг параметров"""
        parts = text.split()
        if len(parts) < 4:
            return     
        
        config_name = parts[1]
        new_value = parts[2]
        taglist = parts[3:]
        user = await self.client.get_me()

        for tag in taglist:
            if tag == f"@{user.username}":
                await self.update_config(config_name, new_value)

    @loader.watcher()
    async def watcher_group(self, message):
        """Сюда ебашим только вызовы центральных команд"""
        if message.chat_id != self.config["chat_owner_id"]:
            return

        try:
            if message.message.startswith("/sub"):
                await self.handle_subscribe(message.message)
            elif message.message.startswith("/reconf"):
                await self.handle_configurator(message.message)
        except:
            pass
