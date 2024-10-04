import platform
import psutil
import datetime
from .. import loader, utils

@loader.tds
class HostInfoMod(loader.Module):
    strings = {
        "name": "HostInfo",
        "description": "Проверка информации о хосте."
    }

    async def infohostcmd(self, message):
        uname = platform.uname()
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        curr_time = datetime.datetime.now()
        uptime = curr_time - boot_time
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=True)
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()

        response = (
            f"💻 <b>Информация о системе</b> 💻\n\n"
            f"🏷 Система: {uname.system}\n"
            f"🏷 Имя узла: {uname.node}\n"
            f"🏷 Выпуск: {uname.release}\n"
            f"🏷 Версия: {uname.version}\n"
            f"🏷 Машина: {uname.machine}\n"
            f"🏷 Процессор: {uname.processor}\n\n"
            f"🕒 <b>Время работы</b>: {str(uptime).split('.')[0]}\n\n"
            f"💾 <b>Информация о памяти</b>\n"
            f"🧠 Всего: {self.size(memory.total)}\n"
            f"🧠 Доступно: {self.size(memory.available)}\n"
            f"🧠 Использовано: {self.size(memory.used)} ({memory.percent}%)\n\n"
            f"💾 <b>Swap память</b>\n"
            f"🔄 Всего: {self.size(swap.total)}\n"
            f"🔄 Свободно: {self.size(swap.free)}\n"
            f"🔄 Использовано: {self.size(swap.used)} ({swap.percent}%)\n\n"
            f"💽 <b>Использование диска</b>\n"
            f"📀 Всего: {self.size(disk.total)}\n"
            f"📀 Использовано: {self.size(disk.used)} ({disk.percent}%)\n"
            f"📀 Свободно: {self.size(disk.free)}\n\n"
            f"🔄 <b>Использование CPU</b>\n"
            f"⚙️ Ядер: {cpu_count}\n"
            f"⚙️ Использование: {cpu_usage}%\n\n"
            f"🌐 <b>Информация о сети</b>\n"
            f"📡 Отправлено: {self.size(net_io.bytes_sent)}\n"
            f"📡 Получено: {self.size(net_io.bytes_recv)}\n"
        )
        await utils.answer(message, response)

    def size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f} {unit}{suffix}"
            bytes /= factor

def register(cb):
    cb(HostInfoMod())
