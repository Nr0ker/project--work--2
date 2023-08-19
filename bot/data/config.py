from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = "6134050209:AAF4BFPnmo3rRj1H8htJmXkIVM2ob61QB-s"

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
