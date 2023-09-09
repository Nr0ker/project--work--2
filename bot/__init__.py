from bot.data.config import dp, bot, ADMINS
from bot.set_default_commands import set_default_commands
from aiogram import types
from bot.keyboards import kb_resume, kb_yes_no
from bot import anket
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import mysql.connector
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

user_id = None


@dp.message_handler(commands="start")
async def start(message: types.Message):
    global user_id
    await bot.send_message(text=" Вітаємо вас у нашому боті для заявки на роботу! 🌟 "
                                "\nТут ви зможете легко і швидко подати заявку на цікаву вакансію або розмістити своє резюме. "
                                "\nПросто заповніть пункти які наведені нижче, введіть команду /confirm - для обробки ваших данних, "
                                "\nпотім відправте резюме адміністратору з допомогою команди /send_survey ", chat_id=message.from_user.id,  reply_markup=kb_resume)
    user_id = message.from_user.id


@dp.message_handler(commands='send_survey')
async def send_photo_to_admin(message: types.Message):
    with open('anketa.png', 'rb') as photo:
        await bot.send_photo(chat_id=ADMINS, photo=photo, caption="Прийняти?", reply_markup=kb_yes_no)
    await bot.send_photo(message.from_user.id, text="Ваша заяква прийнята, ми вам зателефонуємо")


# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="project--2"
# )
# cursor = db.cursor()


# class ApplyStatesGroup(StatesGroup):
#     apply = State()
#     date = State()
#     send = State()
#

# def generate_keyboard_days():
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     today = datetime.date.today()
#     for i in range(7):
#         date = today + datetime.timedelta(days=i)
#         date_str = date.strftime("%d.%m")
#         callback_data = f"date_{date.strftime('%Y-%m-%d')}"
#         keyboard.add(types.InlineKeyboardButton(text=date_str, callback_data=callback_data))
#     return keyboard

#
# @dp.callback_query_handler(lambda c: c.data == "apply_callback")  # Изменено имя колбэка
# async def chose_variant_yes(variant):
#     answer = "прийнято"
#     sql_query = (f"INSERT INTO resumes (status) VALUES (%s)")
#     await bot.send_message(ADMINS, text="Виберіть дату для співбесіди", reply_markup=generate_keyboard_days())
#     cursor.execute(sql_query, answer)
#     db.commit()
#     cursor.close()
#     await ApplyStatesGroup.next()  # Исправлено на await state.next()
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state=ApplyStatesGroup.date)
# async def apply_date(callback_query: types.CallbackQuery, state: FSMContext):
#     selected_date = callback_query.data.replace('date_', '')
#     sql_query = (f"INSERT INTO resumes (interview_date) VALUES (%s)")
#     cursor.execute(sql_query, selected_date)
#     await ApplyStatesGroup.next()  # Исправлено на await state.reset()
#
#
# @dp.callback_query_handler(lambda c: c.data == "reject_callback")  # Изменено имя колбэка
# async def chose_variant_no(variant):
#     answer = "не прийнято"
#     sql_query = (f"INSERT INTO resumes (status) VALUES (%s)")
#     cursor.execute(sql_query, answer)
#     db.commit()
#     cursor.close()
#     await ApplyStatesGroup.next()  # Исправлено на await state.next()
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state=ApplyStatesGroup.send)
# async def apply(callback_query: types.CallbackQuery, state: FSMContext):
#     user_id = callback_query.from_user.id
#     cursor.execute("SELECT status, interview_date FROM resumes WHERE user_id = %s", (user_id,))
#     result = cursor.fetchone()
#
#     if result:
#         status, interview_date = result
#
#         if status == 'прийнято':
#             await bot.send_message(user_id,
#                                    f"Вас запросили на співбеісду о {interview_date} на 10 годин ранку на /типу ім'я вулиці/")
#         else:
#             await bot.send_message(user_id, "Вибачте, вас не прийняли на роботу.")
#
#     await state.reset_state()
#
# db.close()


@dp.message_handler(commands="help")
async def help(message: types.Message):
    await bot.send_message(text="Цей бот допоможе нам відібрати найкращих працівників у своїй сфері, може ви і є один з них! Заповніть анкету і чекайте відповіді адміністратора, поки вас не запросять на співбесіду."
"\nКоманди можете найти ввів в чат /", chat_id=message.from_user.id)


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

if __name__ == '__main__':
    from aiogram import executor
    from aiogram.types import ParseMode, InlineKeyboardButton

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
