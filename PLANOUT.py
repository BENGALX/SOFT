from telethon.tl.functions.messages import SendMessageRequest
from .. import loader
import asyncio
import re

@loader.tds
class PlanOutMod(loader.Module):
    """Модуль для постепенного вывода тегов.
           Команда: /planout, /stopout.\n
    ⚙️ By BENGAL & @pavlyxa_rezon"""

    strings = {"name": "BGL-PLANOUT"}

    def __init__(self):
        self.stop_event = None

    async def send_message(self, chat_id, message_text):
        try:
            chat_entity = await self.client.get_entity(chat_id)
            await self.client(SendMessageRequest(peer=chat_entity, message=message_text))
        except:
            pass

    async def planning_out(self, chat_id, word_list, delay, trigger):
        if trigger == 'uns':
            logic_used = "BGL-UNSUBSCR"
        elif trigger == 'sub':
            logic_used = "BGL-SUBSCRIBE"
        else:
            logic_used = "NONE"
        
        setting_message = (
            f"⚙️ CONFIGURATION VALUE:\n"
            f"     ├Delay timeout: {delay} min.\n"
            f"     ├Current trigger: /{trigger}.\n"
            f"     └Set logic: {logic_used}.\n"
        )
        await self.send_message(chat_id, setting_message)

        for kusok in word_list:
            if self.stop_event is not None and self.stop_event.is_set():
                return

            if trigger == 'uns':
                if kusok.startswith("https://t.me/"):
                    newtag = kusok.split("https://t.me/", 1)[1].split()[0]
                    output = f"/{trigger} @{newtag}"
                elif kusok.startswith("@"):
                    output = f"/{trigger} {kusok}"
                else:
                    output = f"⚠️ Не распознано: {kusok}"
                await self.send_message(chat_id, output)
                await asyncio.sleep(delay * 60)

            elif trigger == 'sub':
                if kusok.startswith("https://t.me/"):
                    output = f"/{trigger} {kusok}"
                elif kusok.startswith("@"):
                    newlink = kusok.split("@", 1)[1].split()[0]
                    output = f"/{trigger} https://t.me/{newlink}"
                else:
                    output = f"⚠️ Не распознано: {kusok}"
                await self.send_message(chat_id, output)
                await asyncio.sleep(delay * 60)

            else:
                if kusok.startswith("https://t.me/"):
                    output = f"/{trigger} {kusok}"
                elif kusok.startswith("@"):
                    output = f"/{trigger} {kusok}"
                else:
                    output = f"⚠️ Не распознано: {kusok}"
                await self.send_message(chat_id, output)
                await asyncio.sleep(delay * 60)
                
        done_message = f"✅ Вывод завершен успешно."
        await self.send_message(chat_id, done_message)
        self.stop_event = None

    @loader.watcher()
    async def watcher(self, message):
        if message.chat_id != -1002187149618:
            return
        try:
            if message.message.startswith("/planout"):
                user_message = message.message
                shablon_message = message.message.split()
                
                if len(shablon_message) < 4:
                    error_delay = "⚠️ Неправильный формат команды.\n"\
                                    "Шаблон: /planout <delay> <trigger> <text>"
                    await self.send_message(message.chat_id, error_delay)
                    return
                
                if self.stop_event is not None and not self.stop_event.is_set():
                    await_message = f"⏳ Сейчас активен другой процесс вывода.\n"\
                                    f"Дождитесь его завершения или используйте /stopout для остановки."
                    await self.send_message(message.chat_id, await_message)
                    return

                word_list = user_message.split()[1:]
                try:
                    delay = int(word_list[0])
                except ValueError:
                    error_message = "⚠️ Задержку нужно вводить цифрой.\n"
                    await self.send_message(message.chat_id, error_message)
                    return
                    
                trigger = word_list[1]
                text_to_check = " ".join(word_list[2:])
                links_and_tags = re.findall(r"(https?://\S+|@\w+)", text_to_check)

                if not links_and_tags:
                    error_text = "⚠️ Элементы для вывода не обнаружены."
                    await self.send_message(message.chat_id, error_text)
                    return

                self.stop_event = asyncio.Event()
                await self.planning_out(message.chat_id, word_list[2:], delay, trigger)

            elif message.message.startswith("/stopout"):
                if self.stop_event is not None and not self.stop_event.is_set():
                    self.stop_event.set()
                    stop_message = f"⛔️ Процесс вывода остановлен досрочно.\n"
                    await self.send_message(message.chat_id, stop_message)
                else:
                    error_stop = f"⚠️ Нет активного процесса для остановки.\n"
                    await self.send_message(message.chat_id, error_stop)
        except:
            pass
