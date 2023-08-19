from bot.data.config import bot, dp
import requests
from aiogram import types


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    bot.send_message(text="Вітаємо, виберіть місто яке вам підходить", chat_id=message.from_user.id)


