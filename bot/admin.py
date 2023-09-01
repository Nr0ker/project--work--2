from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage





# async def forward_message(message: types.Message):
#     # Здесь вы можете указать chat_id чата, из которого хотите получить сообщение
#     message_id_to_forward = message.text  # Замените на ID сообщения для пересылки
#     try:
#         # Пересылаем сообщение из другого чата в текущий чат
#         await bot.forward_message(chat_id=message.chat.id, from_chat_id=ADMINS, message_id=message_id_to_forward)
#         await message.reply("Сообщение успешно переслано из другого чата.")
#     except Exception as e:
#         await message.reply(f"Произошла ошибка при пересылке сообщения: {str(e)}")

