# meta developer: @your_username
# meta_private: This module is written for personal use, and is not intended for public use, do not distribute it

from .. import loader

import logging

logger = logging.getLogger(__name__)


@loader.tds
class TestLogMod(loader.Module):
    """Простой модуль для проверки логов"""

    strings = {"name": "TestLog"}

    def __init__(self):
        self.config = loader.ModuleConfig()

    async def client_ready(self, client, db):
        self.client = client
        logger.info('TestLogMod is ready and logging works')
        print("TestLogMod is ready and logging works (print statement)")
