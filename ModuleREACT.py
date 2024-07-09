from telethon import functions

@loader.tds
class ReactModule(loader.Module):
    """Модуль для ставки реакций на посты в каналах"""

    async def place_reactions(self, channel_url, post_id):
        try:
            # Получаем информацию о посте
            channel_username, post_id = self.extract_channel_and_post_id(channel_url)
            if not channel_username or not post_id:
                return
            # Получаем сообщение по ID
            post = await self.client.get_messages(channel_username, ids=[int(post_id)])
            # Ставим рандомную положительную реакцию
            await self.client(functions.messages.AddReactionRequest(
                channel_username, post.id, '😊'  # Можно заменить на любую другую реакцию
            ))
        except Exception as e:
            logger.error(f"Ошибка при ставке реакции: {e}")

    @loader.watcher(only_channels=True)
    async def watch_and_react(self, message):
        # Проверяем сообщения только из определенного канала
        if message.chat_id != -1002035849227:
            return
        # Ищем ссылки на посты
        channel_links = re.findall(r'https://t.me/[^/]+/\d+', message.text)
        for link in channel_links:
            await self.place_reactions(link)
