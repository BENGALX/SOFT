from datetime import datetime
from telethon.tl.functions.messages import SendMessageRequest
from .. import loader

@loader.tds
class InfochanMod(loader.Module):
    """Модуль для вывода информации о каналах.
            Команда: /infochan @user [d].\n
    ⚙️ By @pavlyxa_rezon"""

    strings = {"name": "BGL-INFOCHAN"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_uid", -1002205010643, "CustomID",
                validator=loader.validators.Integer(),
            )
        )

    async def send_message(self, list_message, chat_id=None):
        try:
            if chat_id is None:
                chat_id = self.config["custom_uid"]
            chat_entity = await self.client.get_entity(chat_id)
            await self.client(SendMessageRequest(peer=chat_entity, message=list_message, no_webpage=True))
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")

    async def get_subscriptions(self):
        async for dialog in self.client.iter_dialogs():
            if dialog.is_channel and dialog.entity.megagroup is False:
                yield dialog.id, dialog.title, dialog.entity.username

    async def get_days_inactive(self, channel_id):
        try:
            async for message in self.client.iter_messages(channel_id, limit=1):
                if message.date is not None:
                    last_post_datetime = message.date
                    now = datetime.now(last_post_datetime.tzinfo)
                    days_inactive = (now - last_post_datetime).days
                    return days_inactive
            return float('inf')
        except Exception as e:
            print(f"Ошибка получения последнего сообщения: {e}")
            return float('inf')

    async def afklist_sender(self, inactivity_days=None):
        public_channels = []
        private_channels = []
        total_count = 0

        async for dialog_id, title, username in self.get_subscriptions():
            days_inactive = await self.get_days_inactive(dialog_id)

            if inactivity_days is not None and days_inactive <= inactivity_days:
                continue

            days_inactive_text = f"{days_inactive}D" if days_inactive != float('inf') else "∞D"

            if username:
                public_channels.append(f"{days_inactive_text} — @{username}")
            else:
                private_channels.append(f"{days_inactive_text} — ID: {dialog_id} — {title}")
            total_count += 1

        if not public_channels and not private_channels:
            list_message = f"🚫 Нет каналов с периодом AFK {inactivity_days} Day."
        else:
            public_list = "\n".join(public_channels)
            private_list = "\n".join(private_channels)
            list_message = (
                f"🔗 Ваши каналы c AFK {inactivity_days} Day — {total_count}:\n\n"
                f"📗 PUBLIC CHANNELS:\n{public_list or 'NOT FOUND.'}\n\n"
                f"📕 PRIVATE CHANNELS:\n{private_list or 'NOT FOUND.'}"
            )

        await self.send_message(list_message)

    @loader.watcher()
    async def watcher_group(self, message):
        if message.chat_id != self.config["custom_uid"]:
            return

        try:
            if message.message.startswith("/infochan"):
                parts = message.message.split()
                notday_message = f"⚠️ ERROR: [day]. Must /infochan @user [D]."

                if len(parts) >= 2:
                    target_user = parts[1]
                    user = await self.client.get_me()

                    if target_user == f"@{user.username}":
                        if len(parts) >= 3 and parts[2].isdigit():
                            inactivity_days = int(parts[2])
                            await self.afklist_sender(inactivity_days=inactivity_days)
                        else:
                            await self.send_message(notday_message)
        except:
            pass
