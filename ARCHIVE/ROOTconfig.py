    def __init__(self):
        self.module_enabled = True

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

    if message.message.startswith("root"):
        await self.handle_root_config(message.message, message.sender_id)
    if not self.module_enabled:
        return
