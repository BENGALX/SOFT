import re
import asyncio
from .. import loader, utils

from telethon.tl import functions
from telethon.tl.types import Message, PeerChannel

from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, StartBotRequest

@loader.tds
class BENGALSOFTMod(loader.Module):
    """Модуль управления каналами.
           Manual: /man @user\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {
        "name": "BENGALSOFT",
        "manual_basic": (
            "<b>🔗 Базовая настройка:</b>\n"
            "▪️Для начала нужно разделить все ваши аккаунты на условные группы (по умолчанию стоит группа 1). "
            "Делаем группы по 10-15 аккаунтов, по несколько с каждого сервера. "
            "Это создает задержку между выполнениями действий каждой группы в Х*20 секунд.\n\n"
            "▪️Далее на одном из аккаунтов каждой группы нужно включить логгирование (по умолчанию оно выключено). "
            "Так логи будут выводиться только с выбранных аккаунтов прямо в вашу группу.\n\n"
            "<b>🔗 Конфиг: /reconf [name] [value] [acc]</b>\n"
            "▪️logger — булевый статус (True/False, 1/0, yes/no).\n"
            "▪️group — номер сервера или группы аккаунтов.\n"
            "▪️acc — один или несколько юзеров, где нужно перезаписать конфиг (all для всех).\n"
        ),
        "manual_channels": (
            "<b>Текущий функционал модуля:</b>\n\n"
            "<b>🔗 SUBSCRIBE: /sub [target]</b>\n"
            "▪️PUBLIC: https://t.me/, t.me/ or @\n"
            "▪️PRIVATE: https://t.me/+, t.me/+\n\n"
            "<b>🔗 UNSUBSCRIBE: /uns [target]</b>\n"
            "▪️PUBLIC: https://t.me/, t.me/ or @\n"
            "▪️PRIVATE: ID без минуса.\n\n"
            "<b>🔗 BUTTON PUSH: /run [link]</b>\n"
            "▪️PUBLIC: https://t.me/ or t.me/\n"
            "▪️PRIVATE: https://t.me/c/ or t.me/c/\n\n"
            "<b>🔗 REFERAL START: /ref [link]</b>\n"
            "▪️LINK: https://t.me/[BOT]?start=[KEY], t.me/[BOT]?start=[KEY] or [BOT]?start=[KEY]\n"
            "▪️BOTS: @BestRandom_bot @TheFastes_Bot @TheFastesRuBot @GiveawayLuckyBot @best_contests_bot\n\n"
            "<b>Таким образом, с помощью модуля можно подписываться и отписываться от любых каналов и групп, а также участвовать в розыгрышах в обычных и реферальых ботах.</b>\n"
            "<b>Это стартовый модуль начинающего софтера.</b>"
        )
    }
    
    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "logger", False, "Статус работы логгера.",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "group", 1, "Номер группы акков.",
                validator=loader.validators.Integer(),
            )
        )

    async def delay_host(self):
        """Задержка выполняется"""
        delay_seconds = self.get_delay_host()
        await asyncio.sleep(delay_seconds)
        return delay_seconds
    
    def get_delay_host(self):
        """Значение задержки"""
        delay_seconds = self.config["group"] * 20
        return delay_seconds
        
    def get_manual_config(self):
        """Значение manual_config."""
        config_string = ''.join([f"▪️<b>{key}</b> {value}.\n" for key, value in self.config.items()])
        manual_config = (
            "<b>⚙️ BENGALSOFT CONFIG</b>\n\n"
            "<b>Неизменяемые параметры:</b>\n"
            f"▪️<b>owner_list</b> {self.owner_list}.\n"
            f"▪️<b>owner_chat</b> {self.owner_chat}.\n\n"
            "<b>Редактируемые параметры:</b>\n" +
            config_string +
            "\nПримеры изменения конфигурации:\n"
            "/reconf logger True @user1 @user2\n/reconf group 2 all"
        )
        return (manual_config)
    

    async def send_module_message(self, text, delay_info=None):
        """Логи действий модуля"""
        if not self.config["logger"]:
            return
        try:
            delay_text = f", Delay: {delay_info} сек" if delay_info is not None else ""
            logger_message = f"💻 <b>Server: {self.config['group']}{delay_text}</b>\n{text}"
            await self.client.send_message(self.owner_chat, logger_message, link_preview=False)
        except:
            pass

    async def send_manual_message(self):
        """Вывод мануала по модулю"""
        try:
            image_url = "https://raw.githubusercontent.com/BENGALX/SOFT/bengal/IMAGE/BENGAL.jpg"
            image_cpt = f"<b>⚙️ BENGALSOFT for BENGAL\n💻 By @pavlyxa_rezon"
            next_text = (
            f"<b>⚙️ Список мануалов модуля:\n\n"
            f"<b>Чтобы просмотреть базовую настройку, введите:</b>\n/config @</b>"
            )
            await self.client.send_file(
                self.owner_chat,
                file=image_url,
                caption=image_cpt
            )
            await asyncio.sleep(2)
            await self.client.send_message(self.owner_chat, next_text)
        except Exception as e:
            await self.client.send_message(self.owner_chat, f"🚫 ERROR in send_manual_message: {e}")

    async def send_config_message(self):
        """Вывод текущей конфигурации"""
        try:
            variables = ''.join([f"▪️<b>{key}</b> {value}.\n" for key, value in self.config.items()])
            configuration = (
                "<b>🔒 Константы:</b>\n"
                f"▪️<b>owner_list</b> {self.owner_list}.\n"
                f"▪️<b>owner_chat</b> {self.owner_chat}.\n\n"
                f"<b>🔓 Переменные:</b>\n" +
                variables
            )
            await self.client.send_message(self.owner_chat, configuration)
        except Exception as e:
            await self.client.send_message(self.owner_chat, f"🚫 ERROR in send_configuration_message: {e}")


    
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

    
    async def unsubscribe_tag(self, target):
        """Отписка по юзернейму."""
        done_message = f"<b>✅ UNSUBSCRIBE:</b> {target}"
        user_message = f"<b>✅ DELETE:</b> {target}"
        try:
            await self.client(functions.channels.LeaveChannelRequest(target))
            await self.send_module_message(done_message, delay_info=self.get_delay_host())
        except:
            await self.client.delete_dialog(target)
            await self.send_module_message(user_message, delay_info=self.get_delay_host())

    async def unsubscribe_link(self, target):
        """Отписка по ссылке."""
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

    async def unsubscribe_id(self, target):
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


    
    async def button_private(self, target):
        """Нажатие кнопки в приватных."""
        try:
            chan, post = target.split("t.me/c/")[1].split("/")
            inline_button = await self.client.get_messages(PeerChannel(int(chan)), ids=int(post))
            click = await inline_button.click(data=inline_button.reply_markup.rows[0].buttons[0].data)
            clicked_message = click.message
            log_message = f"<b>✅ BUTTON PUSH:</b> https://t.me/c/{chan}/{post}\n\n{clicked_message}"
            await self.send_module_message(log_message, delay_info=self.get_delay_host())
        except Exception as e:
            await self.send_module_message(f"<b>🚫 ERROR:</b> {e}")

    async def button_public(self, target):
        """Нажатие кнопки в публичных."""
        try:
            chan, post = target.split("t.me/")[1].split("/")
            inline_button = await self.client.get_messages(chan, ids=int(post))
            click = await inline_button.click(data=inline_button.reply_markup.rows[0].buttons[0].data)
            clicked_message = click.message
            log_message = f"<b>✅ BUTTON PUSH:</b> https://t.me/{chan}/{post}\n\n{clicked_message}"
            await self.send_module_message(log_message, delay_info=self.get_delay_host())
        except Exception as e:
            await self.send_module_message(f"<b>🚫 ERROR:</b> {e}")
            

    async def start_ref_bot(self, bot_name, ref_key):
        """Запуск ботов по реферальному ключу."""
        try:
            await self.client(StartBotRequest(bot=bot_name, peer=bot_name, start_param=ref_key))
            await asyncio.sleep(2)
            messages = await self.client.get_messages(bot_name, limit=1)
            response_message = "⚠️ Ошибка, бот не ответил."
            if messages and messages[0].sender_id == (await self.client.get_input_entity(bot_name)).user_id:
                response_message = messages[0].message
            done_message = f"<b>✅ START:</b> @{bot_name}\n\n{response_message}"
            await self.send_module_message(done_message, delay_info=self.get_delay_host())
        except Exception as e:
            error_message = f"<b>🚫 START BOT ERROR:</b> @{bot_name}\n{e}"
            await self.send_module_message(error_message)

    
    async def update_user_config(self, config_name, new_value):
        """Обновление переменных конфигураторов."""
        try:
            if config_name not in self.config:
                raise KeyError(f"Config name '{config_name}' not found")
            else:
                if isinstance(self.config[config_name], bool):
                    new_value = new_value.lower() in ['true', '1', 'yes']
                elif isinstance(self.config[config_name], int):
                    new_value = int(new_value)
                self.config[config_name] = new_value
                done_message = f"<b>✅ CONFIG: {config_name} set to {new_value}.</b>"
                await self.client.send_message(self.owner_chat, done_message)
        except KeyError as e:
            error_message = f"<b>❌ Error: {str(e)}</b>"
            await self.client.send_message(self.owner_chat, error_message)
        except Exception as e:
            error_message = f"<b>❌ Error updating config: {str(e)}</b>"
            await self.client.send_message(self.owner_chat, error_message)

    

    async def handle_manual(self, text):
        """Обработка команды /manual"""
        try:
            parts = text.split()
            if len(parts) < 2:
                return
            user = await self.client.get_me()
            if parts[1] != f"@{user.username}":
                return
            await self.send_manual_message()
        except Exception as e:
            await self.client.send_message(self.owner_chat, f"🚫 ERROR in handle_manual: {e}")
    
    async def handle_subscribe(self, text):
        """Центральная обработка /sub"""
        target = text.split("/sub", 1)[1].strip()
        if 't.me/+' in target:
            await self.delay_host()
            await self.subscribe_private(target)
        elif "t.me/" in target or "@" in target:
            await self.delay_host()
            await self.subscribe_public(target)
        else:
            await self.send_module_message("<b>🚫 SUBSCRIBE ERROR:</b> Неверный формат.")

    async def handle_unsubscribe(self, text):
        """Центральная обработка /uns"""
        target = text.split("/uns", 1)[1].strip()
        if target.startswith("@"):
            await self.delay_host()
            await self.unsubscribe_tag(target)
        elif "t.me/" in target:
            await self.delay_host()
            await self.unsubscribe_link(target)
        elif target.isdigit():
            await self.delay_host()
            await self.unsubscribe_id(target)
        else:
            await self.send_module_message("<b>🚫 UNSUBSCRIBE ERROR:</b> Неверный формат.")

    async def handle_runner(self, text):
        """Центральная обработка /run"""
        try:
            target = text.split("/run", 1)[1].strip()
            if 't.me/c/' in target:
                await self.delay_host()
                await self.button_private(target)
            elif 't.me/' in target:
                await self.delay_host()
                await self.button_public(target)
            else:
                await self.send_module_message(f"<b>🚫 RUN ERROR:</b> {target}")
        except Exception as e:
            await self.send_module_message(f"🚫 ERROR in handle_runner: {e}")
            
    async def handle_referal(self, text):
        """Центральная обработка /ref"""
        bot_name = None
        ref_key = None
        if "BestRandom_bot" in text:
            bot_name = "BestRandom_bot"
        elif "TheFastes_Bot" in text:
            bot_name = "TheFastes_Bot"
        elif "TheFastesRuBot" in text:
            bot_name = "TheFastesRuBot"
        elif "GiveawayLuckyBot" in text:
            bot_name = "GiveawayLuckyBot"
        elif "best_contests_bot" in text:
            bot_name = "best_contests_bot"
        if bot_name:
            match = re.search(r"\?start=([\w-]+)", text)
            if match:
                ref_key = match[1]
                await self.delay_host()
                await self.start_ref_bot(bot_name, ref_key)
            else:
                await self.send_module_message(f"<b>🚫 REFERAL ERROR:</b> ref_key для @{bot_name} не найден.")
        else:
            await self.send_module_message(f"<b>🚫 REFERAL ERROR:</b> бот не распознан в: {text}")
    
    async def handle_user_config(self, text):
        """Обработка USER команды /config"""        
        parts = text.split()
        if len(parts) < 3:
            return
        action = parts[1]
        user = await self.client.get_me()
        if action == "set":
            if len(parts) < 4:
                return
            config_name = parts[2]
            new_value = parts[3]
            taglist = parts[4:]
            if "all" in taglist:
                await self.update_user_config(config_name, new_value)
            else:
                for tag in taglist:
                    if tag == f"@{user.username}":
                        await self.update_user_config(config_name, new_value)
        else:
            taglist = parts[1:]
            if "all" in taglist or any(tag == f"@{user.username}" for tag in taglist):
                await self.send_config_message()

    
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
            elif message.message.startswith("/run"):
                await self.handle_runner(message.message)
            elif message.message.startswith("/ref"):
                await self.handle_referal(message.message)
            elif message.message.startswith("/manual"):
                await self.handle_manual(message.message)
            elif message.message.startswith("/config"):
                await self.handle_user_config(message.message)
        except:
            pass
