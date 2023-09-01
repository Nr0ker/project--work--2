from bot.data.config import dp, bot, ADMINS
from aiogram import types
from keyboards import kb_yes_no
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio


@dp.message_handler(commands=['send_anketa'])
async def send_photo_to_admin(message: types.Message):
    admin_user_id = ADMINS  # Замените на ID администратора
    photo_path = 'anketa.png'  # Путь к вашей фотографии

    # Отправка фотографии администратору
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(chat_id=admin_user_id, photo=photo, caption="Ваша фотография", reply_markup=kb_yes_no)

@dp.callback_query_handler(text="apply_callabck")
async def Apply(message: types.Message):
    await bot.send_message(chat_id=ADMINS, text="Назначте дату на співбесіду")
    await bot.send_message(chat_id=message.from_user.id, text="Ви прийняті!!")




# async def forward_message(message: types.Message):
#     # Здесь вы можете указать chat_id чата, из которого хотите получить сообщение
#     message_id_to_forward = message.text  # Замените на ID сообщения для пересылки
#     try:
#         # Пересылаем сообщение из другого чата в текущий чат
#         await bot.forward_message(chat_id=message.chat.id, from_chat_id=ADMINS, message_id=message_id_to_forward)
#         await message.reply("Сообщение успешно переслано из другого чата.")
#     except Exception as e:
#         await message.reply(f"Произошла ошибка при пересылке сообщения: {str(e)}")

