import asyncio, re
from .. import loader, utils

from telethon import TelegramClient
from telethon.tl import functions
from telethon.tl.types import Message, PeerChannel, Channel

from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, StartBotRequest, GetMessagesViewsRequest

from telethon.errors.rpcerrorlist import UserNotParticipantError

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
            f"▪️https://t.me/, t.me/, @ — публичные ссылки, тег.\n"
            f"▪️https://t.me/c/, t.me/c/ — приватные ссылки на пост.\n"
            f"▪️https://t.me/+, t.me/joinchat/ — приватные инвайты.\n"
            f"\n\n"
            f"В подписках, отписках, кнопке, рефе по умолчанию стоит мультиплаер задержки Х20. "
            f"Если нужен другой — вторым аргументом добавляем число: <code>/sub [M] [target]</code>."
            f"\n\n"
            f"<b>🔗 SUBSCRIBE: /sub [target]</b>\n"
            f"▪Тег, ссылка или инвайт в любом формате.\n\n"
            f"<b>🔗 UNSUBSCRIBE: /uns [target]</b>\n"
            f"▪Тег, ссылка либо айди.\n\n"
            f"<b>🔗 BUTTON: /run [link]</b>\n"
            f"▪️Ссылка на пост с кнопкой.\n\n"
            f"<b>🔗 REF START: /ref [link]</b>\n"
            f"▪️Отправляете реферальную ссылку на нужного бота. Поддерживаемые: "
            f"@BestRandom_bot @TheFastes_Bot @TheFastesRuBot @GiveawayLuckyBot @best_contests_bot\n\n"
        ),
        "manual_basic": (
            f"<b>🔐 Команда настройки</b>\n"
            f"<code>/config set</code> [p] [nv] [us]\n"
            f"▪️[p] — имя переменной\n"
            f"▪️[nv] — новое значение\n"
            f"▪️[us] — @(1 |неск.| all)\n\n"
            f"<b>⚙️ Базовая настройка</b>\n"
            "Для начала нужно разделить все аккаунты на виртуальные группы (изначально стоит 1). "
            f"Не путайте группу (пачка твинков, их много) с группой (чат, у нас он один). Их ставим по 5-10 акков. "
            f"Это множитель задержки х20 сек, выставляется числом. Например:\n"
            f"<code>/config set group 2 @u1</code>\n"
            f"<code>/config set group 5 @u5 @u7</code>\n\n"
            f"Далее на одном из акков каждой группы нужно включить логгирование (по умолчанию оно выключено). "
            f"Логгер у нас булевый — принимает значения True/False, 1/0, on/off и т.п. Например:\n"
            f"<code>/config set logger 1 @u1 @u6</code>\n"
            f"<code>/config set logger False all</code>\n"
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

    async def get_config_info(self):
        """Информация о конфигурации."""
        variables = ''.join([f"▪️<b>{key}</b> {value}.\n" for key, value in self.config.items()])
        configuration = (
            f"<b>🔒 Константы:</b>\n"
            f"▪️<b>owner_list</b> {self.owner_list}.\n"
            f"▪️<b>owner_chat</b> {self.owner_chat}.\n"
            f"▪️<b>owner_logs</b> {self.owner_logs}.\n\n"
            f"<b>🔐 Переменные:</b>\n" + variables
        )
        return configuration
    

    async def send_done_message(self, text, delay_info=None):
        """Логи успешных действий модуля"""
        try:
            if not self.config["logger"]:
                return
            if delay_info is not None:
                mult, delay_s = delay_info
                delay_text = f", M: x{mult}, KD: {delay_s} sec."
            else:
                delay_text = ", Delay NONE"
            logger_message = f"💻 <b>GROUP: {self.config['group']}{delay_text}</b>\n{text}"
            await self.client.send_message(self.owner_logs, logger_message, link_preview=False)
        except:
            pass

    async def send_else_message(self, text):
        """Логи действий модуля"""
        try:
            if not self.config["logger"]:
                return
            logger_message = f"{text}"
            await self.client.send_message(self.owner_logs, logger_message, link_preview=False)
        except:
            pass

    async def send_custom_message(self, custom_text):
        """Выводы любыхх текстов."""
        try:
            custom_text = f"{custom_text}"
            await self.client.send_message(self.owner_chat, custom_text, link_preview=False)
        except Exception as e:
            await self.client.send_message(self.owner_chat, f"🚫 ERROR: {e}")

    async def send_manual_message(self, twink):
        """Вывод мануала по модулю"""
        try:
            image_url = "https://raw.githubusercontent.com/BENGALX/SOFT/bengal/IMAGE/BENGAL.jpg"
            image_cpt = f"<b>⚙️ BENGALSOFT for BENGAL\n💻 By @pavlyxa_rezon"
            twink = twink
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
            await self.client.send_message(self.owner_chat, f"🚫 ERROR: {e}")

    async def send_spam_message(self, target, message_text, mult, delay_s):
        """Сообщение в указанный чат."""  
        try:
            chat_entity = await self.client.get_entity(target)
            await self.client.send_message(peer=chat_entity, message=message_text)
            await self.send_done_message(f"<b>♻️ SPAM: {target}</b>", delay_info=(mult, delay_s))
        except Exception as e:
            await self.send_done_message(f"🚫 SPAM: {e}", delay_info=(mult, delay_s))

    
    
    async def subscribe_public(self, target, mult, delay_s):
        """Подписывается на публичные."""
        try:
            if target.startswith("@"):
                chan = target[1:]
            elif "t.me/" in target:
                chan = target.split("t.me/")[1].split("/")[0]
            else:
                await self.send_done_message(f"<b>🚫 SUBSCR: INVALID LINK.</b>", delay_info=(mult, delay_s))
                return
            link = f"https://t.me/{chan}"
            target_entity = await self.client.get_entity(link)
            try:
                await self.client(JoinChannelRequest(channel=chan))
                view_result = await self.views_post(self.client, channel_id=target_entity.id)
                await self.send_done_message(f"<b>♻️ SUBSCR <a href='{link}'>PUBLIC</a>{view_result}</b>", delay_info=(mult, delay_s))
            except Exception as e:
                if "You have joined too many channels/supergroups (caused by JoinChannelRequest)" in str(e):
                    await self.send_done_message(f"<b>🚫 SUBSCR: ACC OWERFLOWING.</b>", delay_info=(mult, delay_s))
                elif "Cannot cast InputPeerUser to any kind of InputChannel." in str(e):
                    await self.send_done_message(f"<b>🚫 SUBSCR: ITS ACCOUNT.</b>", delay_info=(mult, delay_s))
        except Exception as e:
            if any(substring in str(e) for substring in [
                "No user has", "Invalid username",
                "Nobody is using this username, or the username is unacceptable",
                "Cannot find any entity corresponding"
            ]):
                await self.send_done_message(f"<b>🚫 SUBSCR: INVALID ENTITY.</b>", delay_info=(mult, delay_s))
            else:
                await self.send_done_message(f"<b>🚫 SUBSCR PUBLIC:</b> {e}", delay_info=(mult, delay_s))

    async def subscribe_private(self, target, mult, delay_s):
        """Подписывается на частные."""
        try:
            if "t.me/+" in target:
                invite_hash = target.split("t.me/+")[1]
            elif "t.me/joinchat/" in target:
                invite_hash = target.split("t.me/joinchat/")[1]
            else:
                await self.send_done_message(f"<b>🚫 SUBSCR: INVALID LINK.</b>", delay_info=(mult, delay_s))
                return
            await self.client(ImportChatInviteRequest(invite_hash))
            view_result = f", VIEW 0."
            await self.send_done_message(f"<b>♻️ SUBSCR <a href='{target}'>PRIVATE</a>{view_result}</b>", delay_info=(mult, delay_s))
        except Exception as e:
            if "RPCError 400: INVITE_REQUEST_SENT (caused by ImportChatInviteRequest)" in str(e):
                await self.send_done_message(f"<b>⚠️ SUBSCR: INV REQUEST SENT.</b>", delay_info=(mult, delay_s))
            elif "The authenticated user is already a participant of the chat (caused by ImportChatInviteRequest)" in str(e):
                await self.send_done_message(f"<b>⚠️ SUBSCR: ALREADY THERE.</b>", delay_info=(mult, delay_s))
            elif "You have joined too many channels/supergroups" in str(e):
                await self.send_done_message(f"<b>🚫 SUBSCR: ACC OWERFLOWING.</b>", delay_info=(mult, delay_s))
            elif "The chat the user tried to join has expired and is not valid anymore (caused by ImportChatInviteRequest)" in str(e):
                await self.send_done_message(f"<b>🚫 SUBSCR: INVALID ENTITY.</b>", delay_info=(mult, delay_s))
            else:
                await self.send_done_message(f"<b>🚫 SUBSCR PRIVATE:</b> {e}", delay_info=(mult, delay_s))


    
    async def unsubscribe_public(self, target, mult, delay_s):
        """Отписка/удаление по тегу или публичной ссылке."""
        try:
            if target.startswith("@"):
                username = target[1:]
                link = f"https://t.me/{username}"
            elif "t.me" in target:
                try:
                    chan = target.split("t.me/")[1].split("/")[0]
                    link = f"https://t.me/{chan}"
                except IndexError:
                    await self.send_done_message(f"<b>🚫 UNSUB: INVALID LINK.</b>", delay_info=(mult, delay_s))
                    return
                username = chan
            else:
                await self.send_done_message(f"<b>🚫 UNSUB: INVALID LINK.</b>", delay_info=(mult, delay_s))
                return
            await self.client.get_entity(username)
            try:
                await self.client(functions.channels.LeaveChannelRequest(username))
                await self.send_done_message(f"<b>♻️ UNSUB by <a href='{link}'>PUBLIC.</a></b>", delay_info=(mult, delay_s))
            except UserNotParticipantError:
                await self.send_done_message(f"<b>⚠️ UNSUB: NONE IN <a href='{link}'>PUBLIC.</a></b>", delay_info=(mult, delay_s))
            except:
                await self.client.delete_dialog(username)
                await self.send_done_message(f"<b>♻️ DELETE Chat by <a href='{link}'>PUBLIC.</a></b>", delay_info=(mult, delay_s))
        except ValueError:
            await self.send_done_message(f"<b>🚫 UNSUB: INVALID ENTITY.</b>", delay_info=(mult, delay_s))
        except Exception as e:
            await self.send_done_message(f"<b>🚫 UNSUB PUBLIC:</b> {e}", delay_info=(mult, delay_s))

    async def unsubscribe_id(self, target, mult, delay_s):
        """Отписка/удаление по айди или приватной ссылке."""
        try:
            if "t.me/c/" in target:
                chan = target.split("t.me/c/")[1].split("/")[0]
                channel_id = int(chan)
                link = f"https://t.me/c/{channel_id}"
            elif target.isdigit():
                channel_id = int(target)
                link = f"https://t.me/c/{channel_id}"
            else:
                await self.send_done_message(f"<b>🚫 UNSUB: INVALID LINK.</b>", delay_info=(mult, delay_s))
                return
            await self.client(functions.channels.LeaveChannelRequest(channel_id))
            await self.send_done_message(f"<b>♻️ UNSUB by <a href='{link}'>PRIVATE.</a></b>", delay_info=(mult, delay_s))
        except ValueError:
            await self.send_done_message(f"<b>🚫 UNSUB: ID NOT FOUND.</b>", delay_info=(mult, delay_s))
        except Exception as e:
            if "Cannot cast InputPeerUser to any kind of InputChannel" in str(e):
                await self.client.delete_dialog(channel_id)
                await self.send_done_message(f"<b>♻️ DELETE by <a href='{link}'>PRIVATE.</a></b>", delay_info=(mult, delay_s)) 
            elif "The channel specified is private and you lack permission to access it." in str(e):
                await self.send_done_message(f"<b>⚠️ UNSUB: NONE IN <a href='{link}'>PRIVATE.</a></b>", delay_info=(mult, delay_s))
            else:
                await self.send_done_message(f"<b>🚫 UNSUB ID:</b> {e}", delay_info=(mult, delay_s))


    
    async def button_private(self, target, mult, delay_s):
        """Нажатие кнопки в приватных."""
        try:
            try:
                chan, post = target.split("t.me/c/")[1].split("/")
            except ValueError:
                await self.send_done_message(f"<b>🚫 PUSH PRIVATE: FORMAT 1.</b>", delay_info=(mult, delay_s))
                return
            inline_button = await self.client.get_messages(PeerChannel(int(chan)), ids=int(post))
            if not inline_button or not hasattr(inline_button, 'reply_markup') or not inline_button.reply_markup:
                await self.send_done_message(f"<b>🚫 PUSH PRIVATE: NO BUTTON.</b>", delay_info=(mult, delay_s))
                return
            try:
                click = await inline_button.click(data=inline_button.reply_markup.rows[0].buttons[0].data)
            except AttributeError:
                await self.send_done_message(f"<b>🚫 PUSH PRIVATE: NO BUTTON.</b>", delay_info=(mult, delay_s))
            clicked_message = click.message
            view_result = await self.views_post(self.client, channel_id=int(chan), last_message_id=int(post))
            log_message = f"<b>♻️ PUSH <a href='{target}'>PRIVATE</a>{view_result}</b>\n\n{clicked_message}"
            await self.send_done_message(log_message, delay_info=(mult, delay_s))
        except Exception as e:
            if any(substring in str(e) for substring in [
                "Could not find the input entity for PeerChannel",
                "The channel specified is private"
            ]):
                await self.send_done_message(f"<b>🚫 PUSH PRIVATE: NO MEMBER.</b>", delay_info=(mult, delay_s))
            elif "not enough values to unpack" in str(e):
                await self.send_done_message(f"<b>🚫 PUSH PRIVATE: FORMAT 2.</b>", delay_info=(mult, delay_s))
            elif "'NoneType' object has no attribute" in str(e):
                await self.send_done_message(f"<b>🚫 PUSH PRIVATE: CLICK FAIL.</b>", delay_info=(mult, delay_s))
            else:
                await self.send_done_message(f"<b>🚫 PUSH PRIVATE: </b>{e}", delay_info=(mult, delay_s))

    async def button_public(self, target, mult, delay_s):
        """Нажатие кнопки в публичных."""
        try:
            try:
                chan, post = target.split("t.me/")[1].split("/")
            except ValueError:
                await self.send_done_message(f"<b>🚫 PUSH PUBLIC: FORMAT 1.</b>", delay_info=(mult, delay_s))
                return
            channel_entity = await self.client.get_entity(chan)
            inline_button = await self.client.get_messages(chan, ids=int(post))
            if not inline_button or not hasattr(inline_button, 'reply_markup') or not inline_button.reply_markup:
                await self.send_done_message(f"<b>🚫 PUSH PUBLIC: NO BUTTON.</b>", delay_info=(mult, delay_s))
                return
            try:
                click = await inline_button.click(data=inline_button.reply_markup.rows[0].buttons[0].data)
            except AttributeError:
                await self.send_done_message(f"<b>🚫 PUSH PUBLIC: NO BUTTON.</b>", delay_info=(mult, delay_s))
            clicked_message = click.message
            view_result = await self.views_post(self.client, channel_id=channel_entity.id, last_message_id=int(post))
            log_message = f"<b>♻️ PUSH <a href='{target}'>PUBLIC</a>{view_result}</b>\n\n{clicked_message}"
            await self.send_done_message(log_message, delay_info=(mult, delay_s))
        except Exception as e:
            if "not enough values to unpack" in str(e):
                await self.send_done_message(f"<b>🚫 PUSH PUBLIC: FORMAT 2.</b>", delay_info=(mult, delay_s))
            elif "'NoneType' object has no attribute" in str(e):
                await self.send_done_message(f"<b>🚫 PUSH PUBLIC: CLICK FAIL.</b>", delay_info=(mult, delay_s))
            else:
                await self.send_done_message(f"<b>🚫 PUSH PUBLIC: </b>{e}", delay_info=(mult, delay_s))

    
    
    async def start_ref_bot(self, bot_name, ref_key, mult, delay_s):
        """Запуск ботов по реферальному ключу."""
        try:
            await self.client(StartBotRequest(bot=bot_name, peer=bot_name, start_param=ref_key))
            await asyncio.sleep(2)
            messages = await self.client.get_messages(bot_name, limit=1)
            response_message = "⚠️ Ошибка, бот не ответил."
            if messages and messages[0].sender_id == (await self.client.get_input_entity(bot_name)).user_id:
                response_message = messages[0].message
            link = f"https://t.me/{bot_name}?start={ref_key}"
            done_message = f"<b>♻️ START BOT: <a href='{link}'>REFERAL KEY.</a></b>\n\n{response_message}"
            await self.send_done_message(done_message, delay_info=(mult, delay_s))
        except Exception as e:
            error_message = f"<b>🚫 START:</b> @{bot_name}\n{e}"
            await self.send_done_message(error_message, delay_info=(mult, delay_s))

    
    
    async def views_post(self, client, channel_id=None, last_message_id=None):
        """Шарманка для накрута просмотров постов."""
        try:
            if last_message_id is not None:
                await client(GetMessagesViewsRequest(peer=channel_id, id=[last_message_id], increment=True))
                return f", VIEW POST."
            elif channel_id is not None:
                messages = await client.get_messages(channel_id, limit=5)
                message_ids = [msg.id for msg in messages]
                if message_ids:
                    await client(GetMessagesViewsRequest(peer=channel_id, id=message_ids, increment=True))
                    return f", VIEW (L{len(message_ids)})."
                else:
                    return f""
            else:
                return f""
        except Exception as e:
            return f", ERR {e}"
            

    
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
                    manual_text = self.strings["manual_basic"]
                elif parts[1] == "command":
                    manual_text = self.strings["manual_command"]
                await self.send_custom_message(manual_text)
            elif parts[1] == twink:
                await self.send_manual_message(twink)
        except:
            pass
    
    async def handle_subscribe(self, text):
        """Центральная обработка /sub"""
        try:
            parts = text.split()
            if len(parts) < 2:
                return
            mult = int(parts[1]) if parts[1].isdigit() else None
            target = parts[2].strip() if mult else parts[1].strip()
            mult, delay_s = self.get_delay_host(mult)
            if 't.me/+' in target or 't.me/joinchat/' in target:
                await self.delay_host(delay_s)
                await self.subscribe_private(target, mult, delay_s)
            elif "t.me/" in target or "@" in target:
                await self.delay_host(delay_s)
                await self.subscribe_public(target, mult, delay_s)
            else:
                await self.send_else_message("<b>🚫 HANDLE SUB: FORMAT.</b>")
        except Exception as e:
            await self.send_else_message(f"<b>🚫 HANDLE SUB:</b> {e}")

    async def handle_unsubscribe(self, text):
        """Центральная обработка /uns"""
        try:
            parts = text.split()
            if len(parts) < 2:
                return
            mult = int(parts[1]) if parts[1].isdigit() else None
            target = parts[2].strip() if mult else parts[1].strip()
            mult, delay_s = self.get_delay_host(mult)
            if target.isdigit() or "t.me/c/" in target:
                await self.delay_host(delay_s)
                await self.unsubscribe_id(target, mult, delay_s)
            elif 't.me/+' in target:
                await self.send_else_message("<b>🚫 HANDLE UNS: FORMAT.</b>")
            elif target.startswith("@") or "t.me/" in target:
                await self.delay_host(delay_s)
                await self.unsubscribe_public(target, mult, delay_s)
            else:
                await self.send_else_message("<b>🚫 HANDLE UNS: FORMAT.</b>")
        except Exception as e:
            await self.send_else_message(f"<b>🚫 HANDLE UNS:</b> {e}")

    async def handle_runner(self, text):
        """Центральная обработка /run"""
        try:
            parts = text.split()
            if len(parts) < 2:
                return
            mult = int(parts[1]) if parts[1].isdigit() else None
            target = parts[2].strip() if mult else parts[1].strip()
            mult, delay_s = self.get_delay_host(mult)
            if 't.me/c/' in target:
                await self.delay_host(delay_s)
                await self.button_private(target, mult, delay_s)
            elif 't.me/' in target:
                await self.delay_host(delay_s)
                await self.button_public(target, mult, delay_s)
            else:
                await self.send_else_message(f"<b>🚫 HANDLE RUN: FORMAT.</b>")
        except Exception as e:
            await self.send_else_message(f"<b>🚫 HANDLE RUN:</b> {e}")
            
    async def handle_referal(self, text):
        """Центральная обработка /ref"""
        try:
            parts = text.split()
            if len(parts) < 2:
                return
            mult = int(parts[1]) if parts[1].isdigit() else None
            target = parts[2].strip() if mult else parts[1].strip()
            mult, delay_s = self.get_delay_host(mult)
            sup_bot = [
                "BestRandom_bot", "best_contests_bot", "GiveawayLuckyBot",
                "TheFastes_Bot", "TheFastesRuBot"
            ]
            bot_name = next((bot for bot in sup_bot if bot in target), None)
            if not bot_name:
                return await self.send_else_message(f"<b>🚫 HANDLE REF:</b> bot_name not found.")
            match = re.search(r"\?start=([\w-]+)", text)
            if not match:
                return await self.send_else_message(f"<b>🚫 HANDLE REF:</b> ref_key not found.")
            ref_key = match[1]
            await self.delay_host(delay_s)
            await self.start_ref_bot(bot_name, ref_key, mult, delay_s)
        except Exception as e:
            await self.send_else_message(f"<b>🚫 HANDLE REF:</b> {e}")
    
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
                custom_text = await self.get_config_info()
                await self.send_custom_message(custom_text)
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

    async def handle_spamer(self, text):
        """Центральная обработка /sms"""
        try:
            parts = text.split()
            if len(parts) < 3:
                return
            mult = int(parts[1]) if parts[1].isdigit() else None
            target = parts[2].strip() if mult else parts[1].strip()
            mult, delay_s = self.get_delay_host(mult)
            if not (target.startswith("@") or re.match(r"https?://t\.me/", target)):
                await self.send_else_message(f"<b>🚫 HANDLE MESS: TARGET</b>")
                return
            message_text = parts[3] if mult else parts[2]
            await self.delay_host(delay_s)
            await self.send_spam_message(target, message_text, mult, delay_s)
        except Exception as e:
            await self.send_else_message(f"<b>🚫 HANDLE MESS:</b> {e}")

    
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
            elif message.message.startswith("/sms"):
                await self.handle_spamer(message.message)
            elif message.message.startswith("/react"):
                await self.handle_reactor(message.message)
            else:
                return
        except:
            pass
