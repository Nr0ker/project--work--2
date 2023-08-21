from aiogram.utils import executor
from bot.data.config import dp, bot
from bot.set_default_commands import set_default_commands
from aiogram import types
from bot.keyboards import kb
from bot.statesfile import StepStates


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await bot.send_message(text="Вітаємо, виберіть місто в якому ви хочете знайти роботу", chat_id=message.from_user.id, reply_markup=kb)
    await StepStates.sity.set()

@dp.message_handler(commands="help")
async def help(message: types.Message):
    await bot.send_message(text="Цей бот допоможе з вибором роботи на сайті robota.ua", chat_id=message.from_user.id)


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


executor.start_polling(dp, on_startup=on_startup, skip_updates=True)