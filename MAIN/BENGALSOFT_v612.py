import re
import asyncio
from .. import loader, utils

from telethon.tl import functions
from telethon.tl.types import Message, PeerChannel

from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, StartBotRequest, GetMessagesViewsRequest

@loader.tds
class BENGALSOFTMod(loader.Module):
    """Основной модуль софтеров.
           Full Info: /manual @\n
    ⚙️ By @pavlyxa_rezon\n"""

    strings = {
        "name": "BENGALSOFT",
        "manual_command": (
            f"<b>⚙️ Функционал модуля</b>\n"
            f"<b>♻️ Примеры форматов:</b>\n"
            f"▪️https://t.me/ — полная\n"
            f"▪️t.me/ — сокращенная\n"
            f"▪️@tag — публичный тег\n\n"
            f"<b>🔗 SUBSCRIBE: /sub [target]</b>\n"
            f"▪️PUBLIC: любые.\n"
            f"▪️PRIVATE: t.me/+\n\n"
            f"<b>🔗 UNSUBSCRIBE: /uns [target]</b>\n"
            f"▪️PUBLIC: любые.\n"
            f"▪️PRIVATE: ID без -\n\n"
            f"<b>🔗 BUTTON PUSH: /run [link]</b>\n"
            f"▪️PUBLIC: t.me/\n"
            f"▪️PRIVATE: t.me/c/\n\n"
            f"<b>🔗 REFERAL START: /ref [link]</b>\n"
            f"▪️[BOT]?start=[KEY]\n"
            f"▪️SUPPORTED BOT:\n@BestRandom_bot\n@TheFastes_Bot\n@TheFastesRuBot\n@GiveawayLuckyBot\n@best_contests_bot\n\n"
        ),
        "manual_basic": (
            f"<b>🔐 Команда настройки</b>\n"
            f"/config set [p] [nv] [us]\n"
            f"▪️[p] — имя переменной\n"
            f"▪️[nv] — новое значение\n"
            f"▪️[us] — @(1 |неск.| all)\n\n"
            f"<b>⚙️ Базовая настройка</b>\n"
            "▪️Для начала нужно разделить все аккаунты на виртуальные группы (изначально стоит 1). "
            f"Не путайте группу (пачка твинков, их много) с группой (чат, у нас он один). Их ставим по 5-10 акков. "
            f"Это множитель задержки х20 сек, выставляется числом. Например:\n"
            f"/config set group 2 @u1\n"
            f"/config set group 5 @u5 @u7\n\n"
            f"▪️Далее на одном из акков каждой группы нужно включить логгирование (по умолчанию оно выключено). "
            f"Логгер у нас булевый — принимает значения True/False, 1/0, on/off и т.п. Например:\n"
            f"/config set logger 1 @u1 @u6\n"
            f"/config set logger False all\n"
        )
    }
    
    def __init__(self):
        self.owner_list = [922318957]
        self.owner_chat = -1002205010643
        self.owner_logs = -1002205010643
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

    async def delay_host(self, delay_s):
        """Задержка выполняется"""
        await asyncio.sleep(delay_s)
    
    def get_delay_host(self, mult=None):
        """Рассчет кастомной задержки"""
        default_mult = 20
        mult = int(mult) if mult else default_mult
        delay_s = self.config["group"] * mult
        return mult, delay_s

    async def get_user_info(self):
        """Информация о пользователе."""
        user = await self.client.get_me()
        if user.username:
            twink = f"@{user.username}"
        else:
            twink = None
        return twink
    

    async def send_done_message(self, text, delay_info=None):
        """Логи успешных действий модуля"""
        try:
            if delay_info is not None:
                mult, delay_s = delay_info
                delay_text = f", M: x{mult}, KD: {delay_s} sec."
            else:
                delay_text = ", Delay NONE"
            logger_message = f"💻 <b>GROUP: {self.config['group']}{delay_text}</b>\n{text}"
            await self.client.send_message(self.owner_logs, logger_message, link_preview=False)
        except:
            pass

    async def send_error_message(self, text):
        """Логи ошибочных действий модуля"""
        try:
            logger_message = f"{text}"
            await self.client.send_message(self.owner_logs, logger_message, link_preview=False)
        except:
            pass

    async def send_manual_message(self):
        """Вывод мануала по модулю"""
        try:
            image_url = "https://raw.githubusercontent.com/BENGALX/SOFT/bengal/IMAGE/BENGAL.jpg"
            image_cpt = f"<b>⚙️ BENGALSOFT for BENGAL\n💻 By @pavlyxa_rezon"
            twink = await self.get_user_info()
            next_text = (
                f"<b>⚙️ Список мануалов модуля:\n\n"
                f"<b>▪️Мануал по настройке:</b>\n<code>/manual basic {twink}</code>\n\n"
                f"<b>▪️Мануал по командам:</b>\n<code>/manual command {twink}</code>\n\n"
                f"<b>▪️Посмотреть настройки:</b>\n<code>/config self {twink}</code>\n"
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
                f"<b>🔒 Константы:</b>\n"
                f"▪️<b>owner_list</b> {self.owner_list}.\n"
                f"▪️<b>owner_chat</b> {self.owner_chat}.\n"
                f"▪️<b>owner_logs</b> {self.owner_logs}.\n\n"
                f"<b>🔐 Переменные:</b>\n" + variables
            )
            await self.client.send_message(self.owner_chat, configuration)
        except Exception as e:
            await self.client.send_message(self.owner_chat, f"🚫 ERROR in send_configuration_message: {e}")

    async def send_basic_message(self):
        """Вывод базовой настройки."""
        try:
            await self.client.send_message(self.owner_chat, self.strings["manual_basic"])
        except Exception as e:
            await self.client.send_message(self.owner_chat, f"🚫 ERROR in send_manual_message: {e}")

    async def send_command_message(self):
        """Вывод примеров команд модуля."""
        try:
            await self.client.send_message(self.owner_chat, self.strings["manual_command"])
        except Exception as e:
            await self.client.send_message(self.owner_chat, f"🚫 ERROR in send_manual_message: {e}")


    
    async def subscribe_public(self, target, mult, delay_s):
        """Подписывается на публичные."""
        try:
            await self.client(JoinChannelRequest(channel=target))
            await self.send_done_message(f"<b>♻️ SUB Public:</b> {target}", delay_info=(mult, delay_s))
        except Exception as e:
            await self.send_done_message(f"<b>🚫 SUB Public:</b> {e}", delay_info=(mult, delay_s))

    async def subscribe_private(self, target, mult, delay_s):
        """Подписывается на частные."""
        try:
            invite_hash = target.split("t.me/+")[1]
            await self.client(ImportChatInviteRequest(invite_hash))
            await self.send_done_message(f"<b>♻️ SUB Private:</b> {target}", delay_info=(mult, delay_s))
        except Exception as e:
            await self.send_done_message(f"<b>🚫 SUB Private:</b> {e}", delay_info=(mult, delay_s))

    
    async def unsubscribe_tag(self, target, mult, delay_s):
        """Отписка по юзернейму."""
        try:
            try:
                await self.client(functions.channels.LeaveChannelRequest(target))
                await self.send_done_message(f"<b>♻️ UNSUB:</b> {target}", delay_info=(mult, delay_s))
            except:
                await self.client.delete_dialog(target)
                await self.send_done_message(f"<b>♻️ DELETE:</b> {target}", delay_info=(mult, delay_s))
        except Exception as e:
            await self.send_done_message(f"<b>🚫 UNSUB tag:</b> {e}", delay_info=(mult, delay_s))

    async def unsubscribe_link(self, target, mult, delay_s):
        """Отписка по ссылке."""
        try:
            match = re.search(r't\.me/([a-zA-Z0-9_]+)', target)
            if match:
                username = match.group(1)
                try:
                    await self.client(functions.channels.LeaveChannelRequest(username))
                    await self.send_done_message(f"<b>♻️ UNSUB:</b>\n{target}", delay_info=(mult, delay_s))
                except:
                    await self.client.delete_dialog(username)
                    await self.send_done_message(f"<b>♻️ DELETE:</b>\n{target}", delay_info=(mult, delay_s))
            else:
                await self.send_done_message("🚫 UNSUB: link not found")
        except Exception as e:
            await self.send_done_message(f"<b>🚫 UNSUB link:</b> {e}", delay_info=(mult, delay_s))

    async def unsubscribe_id(self, target, mult, delay_s):
        """Отписка по айди."""
        try:
            try:
                channel_id = int(target)
                await self.client(functions.channels.LeaveChannelRequest(channel_id))
                await self.send_done_message(f"<b>♻️ UNSUB ID:</b> {target}", delay_info=(mult, delay_s))
            except:
                await self.client.delete_dialog(channel_id)
                await self.send_done_message(f"<b>♻️ DELETE ID:</b> {target}", delay_info=(mult, delay_s))
        except Exception as e:
            await self.send_done_message(f"<b>🚫 UNSUB ID:</b> {e}", delay_info=(mult, delay_s))


    
    async def button_private(self, target):
        """Нажатие кнопки в приватных."""
        try:
            chan, post = target.split("t.me/c/")[1].split("/")
            inline_button = await self.client.get_messages(PeerChannel(int(chan)), ids=int(post))
            click = await inline_button.click(data=inline_button.reply_markup.rows[0].buttons[0].data)
            clicked_message = click.message
            log_message = f"<b>♻️ BUTTON PUSH:</b> https://t.me/c/{chan}/{post}\n\n{clicked_message}"
            await self.send_done_message(log_message, delay_info=self.get_delay_host())
        except Exception as e:
            await self.send_done_message(f"<b>🚫 ERROR:</b> {e}")

    async def button_public(self, target):
        """Нажатие кнопки в публичных."""
        try:
            chan, post = target.split("t.me/")[1].split("/")
            inline_button = await self.client.get_messages(chan, ids=int(post))
            click = await inline_button.click(data=inline_button.reply_markup.rows[0].buttons[0].data)
            clicked_message = click.message
            log_message = f"<b>♻️ BUTTON PUSH:</b> https://t.me/{chan}/{post}\n\n{clicked_message}"
            await self.send_done_message(log_message, delay_info=self.get_delay_host())
        except Exception as e:
            await self.send_done_message(f"<b>🚫 ERROR:</b> {e}")
            

    async def start_ref_bot(self, bot_name, ref_key):
        """Запуск ботов по реферальному ключу."""
        try:
            await self.client(StartBotRequest(bot=bot_name, peer=bot_name, start_param=ref_key))
            await asyncio.sleep(2)
            messages = await self.client.get_messages(bot_name, limit=1)
            response_message = "⚠️ Ошибка, бот не ответил."
            if messages and messages[0].sender_id == (await self.client.get_input_entity(bot_name)).user_id:
                response_message = messages[0].message
            done_message = f"<b>♻️ START:</b> @{bot_name}\n\n{response_message}"
            await self.send_done_message(done_message, delay_info=self.get_delay_host())
        except Exception as e:
            error_message = f"<b>🚫 START BOT ERROR:</b> @{bot_name}\n{e}"
            await self.send_done_message(error_message)

    
    async def update_user_config(self, config_name, new_value):
        """Обновление переменных конфигураторов."""
        try:
            if config_name not in self.config:
                raise KeyError(f"Config name '{config_name}' not found")
            else:
                if isinstance(self.config[config_name], bool):
                    new_value = new_value.lower() in {'true', '1', 'yes', 'on'}
                elif isinstance(self.config[config_name], int):
                    new_value = int(new_value)
                self.config[config_name] = new_value
                done_message = f"<b>♻️ CONFIG: {config_name} set to {new_value}.</b>"
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
            twink = await self.get_user_info()
            if twink is None:
                return
            if len(parts) >= 3 and parts[2] == twink:
                if parts[1] == "basic":
                    await self.send_basic_message()
                elif parts[1] == "command":
                    await self.send_command_message()
            elif parts[1] == twink:
                await self.send_manual_message()
        except:
            pass
    
    async def handle_subscribe(self, text):
        """Центральная обработка /sub"""
        parts = text.split()
        if len(parts) < 2:
            return
        if parts[1].isdigit():
            mult = int(parts[1])
            target = parts[2].strip()
        else:
            mult = None
            target = parts[1].strip()
        mult, delay_s = self.get_delay_host(mult)
        if 't.me/+' in target:
            await self.delay_host(delay_s)
            await self.subscribe_private(target, mult, delay_s)
        elif "t.me/" in target or "@" in target:
            await self.delay_host(delay_s)
            await self.subscribe_public(target, mult, delay_s)
        else:
            await self.send_error_message("<b>🚫 SUB:</b> Неверный формат.")

    async def handle_unsubscribe(self, text):
        """Центральная обработка /uns"""
        parts = text.split()
        if len(parts) < 2:
            return
        if parts[1].isdigit():
            mult = int(parts[1])
            target = parts[2].strip()
        else:
            mult = None
            target = parts[1].strip()
        mult, delay_s = self.get_delay_host(mult)
        if target.startswith("@"):
            await self.delay_host(delay_s)
            await self.unsubscribe_tag(target, mult, delay_s)
        elif "t.me/" in target:
            await self.delay_host(delay_s)
            await self.unsubscribe_link(target, mult, delay_s)
        elif target.isdigit():
            await self.delay_host(delay_s)
            await self.unsubscribe_id(target, mult, delay_s)
        else:
            await self.send_done_message("<b>🚫 UNSUB:</b> Неверный формат.")

    async def handle_runner(self, text):
        """Центральная обработка /run"""
        try:
            parts = text.split()
            if len(parts) < 2:
                return
            target = parts[1].strip()
            if 't.me/c/' in target:
                await self.delay_host()
                await self.button_private(target)
            elif 't.me/' in target:
                await self.delay_host()
                await self.button_public(target)
            else:
                await self.send_done_message(f"<b>🚫 RUN ERROR:</b> {target}")
        except Exception as e:
            await self.send_done_message(f"🚫 ERROR in handle_runner: {e}")
            
    async def handle_referal(self, text):
        """Центральная обработка /ref"""
        bot_name = None
        ref_key = None
        sup_bot = [
            "BestRandom_bot", "best_contests_bot", "GiveawayLuckyBot",
            "TheFastes_Bot", "TheFastesRuBot"
        ]
        parts = text.split()
        if len(parts) < 2:
            return
        target = parts[1]
        for bot in sup_bot:
            if bot in target:
                bot_name = bot
                break
        if bot_name:
            match = re.search(r"\?start=([\w-]+)", text)
            if match:
                ref_key = match[1]
                await self.delay_host()
                await self.start_ref_bot(bot_name, ref_key)
            else:
                await self.send_done_message(f"<b>🚫 REFERAL ERROR:</b> ref_key для @{bot_name} не найден.")
        else:
            await self.send_done_message(f"<b>🚫 REFERAL ERROR:</b> бот не распознан в: {text}")
    
    async def handle_user_config(self, text):
        """Обработка USER команды /config"""
        parts = text.split()
        if len(parts) < 3:
            return
        twink = await self.get_user_info()
        if parts[1] == "set":
            if len(parts) < 4:
                return
            config_name = parts[2]
            new_value = parts[3]
            taglist = parts[4:]
            if "all" in taglist:
                await self.update_user_config(config_name, new_value)
            else:
                for tag in taglist:
                    if tag == twink:
                        await self.update_user_config(config_name, new_value)
        elif parts[1] == "self":
            taglist = parts[2:]
            if "all" in taglist or any(tag == twink for tag in taglist):
                await self.send_config_message()
        else:
            return

    async def handle_user_search(self, text):
        """Обработка USER команды /search"""        
        parts = text.split()
        if len(parts) < 2:
            return
        twink = await self.get_user_info()
        twink_search = parts[1:]
        for tag in twink_search:
            if tag == twink:
                await self.client.send_message(self.owner_chat, f"это я наху {twink}")

    
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
            elif message.message.startswith("/search"):
                await self.handle_user_search(message.message)
        except:
            pass
