from data.config import dp, bot, ADMINS
from aiogram import Dispatcher, types
from keyboards import kb_yes_no
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import mysql.connector
import datetime
from bot.anket import user_id

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'project--2'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


class ApplyStatesGroup(StatesGroup):
    message_id = State()
    apply = State()


@dp.message_handler(commands='send_survey')
async def send_photo_to_admin(message: types.Message, state: FSMContext):
    admin_user_id = ADMINS
    photo_path = 'anketa.png'
    # Отправка фотографии администратору
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(chat_id=admin_user_id, photo=photo, caption="Ваша фотография", reply_markup=kb_yes_no)


@dp.callback_query_handler(text="apply_callabck")
async def Date(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=ADMINS, text="Назначте дату на співбесіду", reply_markup=generate_keyboard_days())
    await ApplyStatesGroup.message_id.set()


@dp.message_handler(state=ApplyStatesGroup.message_id)
async def message(message: types.Message, state: FSMContext):
    message_id = message.from_user.id
    user_message = message.text
    cursor.execute("INSERT INTO message_for_user (message_id, message) VALUES (%s, %s)", (message_id, user_message))
    cursor.close()
    conn.close()
    await ApplyStatesGroup.next()


@dp.callback_query_handler(lambda query: query.data.startswith('set_date:'), state=ApplyStatesGroup.apply)
async def Apply(message: types.Message, callback_query: types.CallbackQuery, state: FSMContext):
    date_str = callback_query.data.split(':')[1]
    selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    query_id = "SELECT * FROM resumes WHERE user_id = %s"
    cursor.execute(query_id, (user_id))
    results = cursor.fetchall()
    await bot.send_message(callback_query.from_user.id, chat_id=results, text=f" Вас запросили на співбеісду о {selected_date} на 10 годин ранку")
    cursor.close()
    conn.close()
    await state.reset_state()


@dp.callback_query_handler(text="reject_callback")
async def Reject(message: types.Message, state: FSMContext):
    query_id = "SELECT * FROM resumes WHERE user_id = %s"
    cursor.execute(query_id, (user_id))
    results = cursor.fetchall()
    await bot.send_message(chat_id=results, text="Вибачайте, ви вас не прийняли на роботу")