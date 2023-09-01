from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
from aiogram.utils import executor
from bot.data.config import dp, bot, ADMINS
from bot.set_default_commands import set_default_commands
from aiogram import types
from bot.keyboards import kb_resume, kb_yes_no
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

pib = ""
birthdate = ""
address = ""
phone_num = ""
communication = ""
email =""
osvita = ""
add = ""


# @dp.message_handler(commands="start")
# async def start(message: types.Message):
#     await bot.send_message(text="Вітаємо, виберіть місто в якому ви хочете знайти роботу", chat_id=message.from_user.id, reply_markup=kb_cities)
#     # await StepStates.sity.set()




# @dp.message_handler(commands="help")
# async def help(message: types.Message):
#     await bot.send_message(text="Цей бот допоможе з вибором роботи на сайті robota.ua;"
#                                 "Команди: /start"
#                                 "/help", chat_id=message.from_user.id)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    global user_id
    await bot.send_message(text="Ми раді вітати вас у команді, яка рухається вперед та росте щодня. Ваша роль - це ключовий елемент нашого успіху, і ми впевнені, що разом ми досягнемо неймовірних результатів.\n"
                                "\nВаша робота допомагає нам знайти талановитих фахівців, які принесуть свої знання та ентузіазм у нашу команду. Ваше завдання - це зробити наш відбір ще кращим, швидшим і більш ефективним.\n"
                                "\nМи віримо в вашу здатність впізнавати істинний потенціал кандидатів та знайти тих, хто буде спільно розвивати нашу компанію. Нехай ваші зусилля завжди будуть винагорожені успішними прийомами на роботу та новими досягненнями.\n"
                                "\nРазом ми зможемо досягти великих вершин, і ми дуже цьому раді. Ще раз ласкаво просимо в нашу команду! Вперед до нових викликів та досягнень!\n"
                                "\nЩоб заповнити заявку використайте команду /do_my_survey"
                                "", chat_id=message.from_user.id)

    with open("it.jpg", 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
    user_id = message.from_user.id

@dp.message_handler(commands="help")
async def help(message: types.Message):
    await bot.send_message(text="Цей бот допоможе вам відправити заявку в IT-компанію."
"\nКоманды: \n1) /start \n2)/help \n3) /do_my_resume \n4) /info", chat_id=message.from_user.id)

@dp.message_handler(commands="do_my_survey")
async def resume(message: types.Message):
    global saved_message, saved_message1, saved_message2
    await bot.send_message(text="Заповніть анкету."
                                "\nЩоб підтвердити використайте /сonfirm", chat_id=message.from_user.id, reply_markup=kb_resume)

class Form(StatesGroup):
    waiting_for_pib = State()

@dp.callback_query_handler(lambda c: c.data == 'LFM_name')
async def process_callback_pib(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть ваші прізвище, ім'я, по батькові: "
                                                      "Щоб подивитися, що ви ввели використайте /get_LFM_name")
    await Form.waiting_for_pib.set()

@dp.message_handler(state=Form.waiting_for_pib)
async def process_pib(message: types.Message, state: FSMContext):
    global pib
    async with state.proxy() as data:
        pib = message.text

    await message.reply("Збережено!")
    await state.finish()

@dp.message_handler(commands=['get_LFM_name'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if pib:
            await message.reply(f"Ваші прізвище, ім'я, по батькові: {pib}")
        else:
            await message.reply("Ви не ввели дані.")

class Form1(StatesGroup):
    waiting_for_birthdaydate = State()

@dp.callback_query_handler(lambda c: c.data == 'birthdate')
async def process_callback_birthdaydate(message: types.Message, state: FSMContext,):
    await bot.send_message(message.from_user.id, text="Введіть вашу дату народження xx:xx:xxxx (число, місяць, рік):"
                                                      "Щоб подивитися, що ви ввели використайте /get_date_of_birth")
    await Form1.waiting_for_birthdaydate.set()


def check_date_format(date):
    pattern = r"(\d{2}):(\d{2}):(\d{4})"
    match = re.match(pattern, date)

    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))

        if 1 <= month <= 12 and 1 <= day <= 31 and year <= 2002:
            return True
    return False

@dp.message_handler(state=Form1.waiting_for_birthdaydate)
async def process_birthdaydate(message: types.Message, state: FSMContext):
    global birthdate
    async with state.proxy() as data:
        birthdate = message.text

    if check_date_format(birthdate):
        print("Дата народження прийнята")
        await message.reply("Данні збережено")
    else:
        await message.reply("Дата рождения не прийнята.")

    await state.finish()


@dp.message_handler(commands=['get_date_of_birth'])
async def get_birthdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if birthdate:
            await message.reply(f"Ваша дата народження: {birthdate}")
        else:
            await message.reply("Ви не ввели дату народження.")

class Form2(StatesGroup):
    waiting_for_adress = State()

@dp.callback_query_handler(lambda c: c.data == 'address')
async def process_callback_adress(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть вашу адресу:"
                                                      "Щоб подивитися, що ви ввели використайте /get_address")
    await Form2.waiting_for_adress.set()

@dp.message_handler(state=Form2.waiting_for_adress)
async def process_adress(message: types.Message, state: FSMContext):
    global address
    async with state.proxy() as data:
        address = message.text

    await message.reply("Адресу збережено")
    await state.finish()

@dp.message_handler(commands=['get_address'])
async def get_adress(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if address:
            await message.reply(f"Ваша адреса: {address}")
        else:
            await message.reply("Ви ще не ввели адресу.")

class Form3(StatesGroup):
    waiting_for_phonenum = State()


def check_phone_format(phone):
    pattern = "/^\+380\d{3}\d{2}\d{2}\d{2}$/"
    if re.match(pattern, phone.replace(" ", "")):
        return True
    return False

@dp.callback_query_handler(lambda c: c.data == 'phone_num')
async def process_callback_pib(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть ваш номер телефону:"
                                                      "Щоб подивитися, що ви ввели використайте /get_phone_num")
    await Form3.waiting_for_phonenum.set()

@dp.message_handler(state=Form3.waiting_for_phonenum)
async def process_pib(message: types.Message, state: FSMContext):
    global phone_num
    async with state.proxy() as data:
        phone_num = message.text

        phone_numbers = [
            "+380 12 345 6789",
            "+380123456789",
            "0661234567",
            "063 123 45 67",
            "050-123-45-67",
            "0671234567",
            "068 123-45-67",
            "123 456 789",
            "999",
        ]

        for number in phone_numbers:
            if check_phone_format(number):
                print(f"Номер '{number}' підходить.")
                await message.reply("Номер збереженно")
            else:
                print(f"Номер '{number}' не підходить.")
                phone_num = ""

        if phone_num == "":
            await message.reply("Номер введено неправильно")
        else:
            pass

        await state.finish()

@dp.message_handler(commands=['get_phone_num'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if phone_num:
            await message.reply(f"Ваш номер телефону: {phone_num}")
        else:
            await message.reply("Вы не ввели номера телефону.")

class Form4(StatesGroup):
    waiting_for_comm = State()

@dp.callback_query_handler(lambda c: c.data == 'communication')
async def process_callback_communication(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть інші способи комунікації:"
                                                      "Щоб подивитися, що ви ввели використайте /get_types_of_communication")
    await Form4.waiting_for_comm.set()

@dp.message_handler(state=Form4.waiting_for_comm)
async def process_communication(message: types.Message, state: FSMContext):
    global communication
    async with state.proxy() as data:
        communication = message.text

    await message.reply("Інформацію збережено")
    await state.finish()

@dp.message_handler(commands=['get_types_of_communication'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if communication:
            await message.reply(f"Інші способи зв'язку: {communication}")
        else:
            await message.reply("Вы еще не ввели інші способи зв'язку.")

class Form5(StatesGroup):
    waiting_for_email = State()
@dp.callback_query_handler(lambda c: c.data == 'email')
async def process_callback_communication(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть інші способи комунікації:"
                                                      "Щоб подивитися, що ви ввели використайте /get_email")
    await Form5.waiting_for_email.set()

@dp.message_handler(state=Form5.waiting_for_email)
async def process_communication(message: types.Message, state: FSMContext):
    global email
    async with state.proxy() as data:
        email = message.text

        await message.reply("Інформацію збережено")

    await state.finish()

@dp.message_handler(commands=['get_email'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if email:
            await message.reply(f"Інші способи зв'язку: {email}")
        else:
            await message.reply("Вы еще не ввели інші способи зв'язку.")


class Form6(StatesGroup):
    waiting_for_osvita = State()

@dp.callback_query_handler(lambda c: c.data == 'education')
async def process_callback_pib(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Початкова загальна освіта", callback_data="education_primary")],
            [InlineKeyboardButton(text="Базова загальна середня освіта", callback_data="education_basic_secondary")],
            [InlineKeyboardButton(text="Повна загальна середня освіта", callback_data="education_full_secondary")],
            [InlineKeyboardButton(text="Професійно-технічна освіта", callback_data="education_professional_technical")],
            [InlineKeyboardButton(text="Неповна вища освіта", callback_data="education_incomplete_higher")],
            [InlineKeyboardButton(text="Базова вища освіта", callback_data="education_basic_higher")],
            [InlineKeyboardButton(text="Повна вища освіта", callback_data="education_full_higher")],
        ]
    )
    await bot.send_message(message.from_user.id, text="Яка у вас освіта:"
                                                      "Щоб подивитися, що ви ввели використайте /get_education", reply_markup=keyboard)
    await Form6.waiting_for_osvita.set()

@dp.callback_query_handler(lambda c: c.data == 'education_primary', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали 'Початкова загальна освіта'")
    global osvita
    async with state.proxy() as data:
        osvita = "Початкова загальна освіта"
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'education_basic_secondary', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Базова загальна середня освіта'")
    global osvita
    async with state.proxy() as data:
        osvita = "Базова загальна середня освіта"
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'education_full_secondary', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Повна загальна середня освіта")
    global osvita
    async with state.proxy() as data:
        osvita = "Повна загальна середня освіта"
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'education_professional_technical', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Професійно-технічна освіта")
    global osvita
    async with state.proxy() as data:
        osvita = "Професійно-технічна освіта"
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'education_incomplete_higher', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Неповна вища освіта")
    global osvita
    async with state.proxy() as data:
        osvita = "Неповна вища освіта"
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'education_basic_higher', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Базова вища освіта")
    global osvita
    async with state.proxy() as data:
        osvita = "Базова вища освіта"
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'education_full_higher', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Повна вища освіта")
    global osvita
    async with state.proxy() as data:
        osvita = "Повна вища освіта"
    await state.finish()

@dp.message_handler(commands=['get_education'])
async def get_osvita(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global osvita
        if osvita:
            await message.reply(f"Ви вибрали: {osvita}")
        else:
            await message.reply("Вы еще не вибрали вашу освіту.")

class Form7(StatesGroup):
    waiting_for_add = State()

@dp.callback_query_handler(lambda c: c.data == 'additional_information')
async def process_callback_add(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Бажаете щось додати?:"
                                                      "Щоб подивитися, що ви додали /get_additional_information")
    await Form7.waiting_for_add.set()

@dp.message_handler(state=Form7.waiting_for_add)
async def process_pib(message: types.Message, state: FSMContext):
    global add
    async with state.proxy() as data:
        add = message.text

    await message.reply("Інформацію збережено!")
    await state.finish()

@dp.message_handler(commands=['get_additional_information'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if add:
            await message.reply(f"Ваші додатки: {add}")
        else:
            await message.reply("Вы еще не ввели додатки.")


def convert_date_format(date):
    try:
        date_obj = datetime.strptime(date, "%d:%m:%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None


@dp.message_handler(commands=['confirm'])
async def confirm_resume(message: types.Message):
    global pib, birthdate, address, phone_num, communication, email, osvita, add

    birthdate = convert_date_format(birthdate)

    # Подключение к базе данных
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Замените на свое имя пользователя MySQL
        password="",  # Замените на свой пароль MySQL
        database="my_resume_db"  # Замените на имя вашей базы данных
    )

    cursor = db.cursor()

    # Вставка данных резюме в таблицу
    cursor.execute("""
        INSERT INTO resumes (pib, birthdate, address, phone_num, communication, email, osvita, add_info)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (pib, birthdate, address, phone_num, communication, email, osvita, add))

    db.commit()
    cursor.close()
    db.close()

    await message.reply("Ваше резюме было успешно сохранено в базе данных!")


    # Создаем изображение
    width, height = 900, 600
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Загружаем шрифт (замените "arial.ttf" на путь к вашему шрифту)
    font = ImageFont.truetype("arial.ttf", 38)

    # Задаем координаты для размещения текста
    x, y = 50, 50
    line_height = 40

    # Заполняем анкету данными
    data = [
        "            Анкета",
        " ",
        f"ФИО: {pib}",
        f"Дата рождения: {birthdate}",
        f"Адрес: {address}",
        f"Телефон: {phone_num}",
        f"Способы связи: {communication}",
        f"Email: {email}",
        f"Образование: {osvita}",
        f"Дополнительно: {add}",
    ]

    # Вставляем данные на изображение
    for item in data:
        draw.text((x, y), item, fill=text_color, font=font)
        y += line_height

    # Сохраняем изображение
    image.save("anketa.png")

    photo_path = 'anketa.png'

    with open(photo_path, 'rb') as photo:
        await bot.send_photo(message.chat.id, types.InputFile(photo))

    pib = ""
    birthdate = ""
    address = ""
    phone_num = ""
    communication = ""
    email = ""
    osvita = ""
    add = ""

from aiogram import Dispatcher, types


@dp.message_handler(commands=['send_survey'])
async def send_photo_to_admin(message: types.Message):
    admin_user_id = ADMINS  # Замените на ID администратора
    photo_path = 'anketa.png'  # Путь к вашей фотографии

    # Отправка фотографии администратору
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(chat_id=admin_user_id, photo=photo, caption="Ваша фотография", reply_markup=kb_yes_no)


@dp.callback_query_handler(text="apply_callabck")
async def Apply(message: types.Message):
    await bot.send_message(chat_id=ADMINS, text="Назначте дату на співбесіду")
    await bot.send_message(chat_id=user_id, text="Ви прийняті!!")

@dp.callback_query_handler(text="reject_callback")
async def Reject(message: types.Message):
    await bot.send_message(chat_id=user_id, text="Вибачайте, але вас не прийняли на роботу")



async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

executor.start_polling(dp, on_startup=on_startup, skip_updates=True)