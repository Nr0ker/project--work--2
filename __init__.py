from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
from aiogram.utils import executor
from bot.data.config import dp, bot
from bot.set_default_commands import set_default_commands
from aiogram import types
from bot.keyboards import kb_resume
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
    await bot.send_message(text="Вітаю, моя айті компанія набирає працівників. \nЩоб подати заявку на роботу введіть /do_my_resume", chat_id=message.from_user.id)

@dp.message_handler(commands="help")
async def help(message: types.Message):
    await bot.send_message(text="Цей бот допоможе вам відправити заявку в IT-компанію."
"\nКоманды: \n1) /start \n2)/help \n3) /do_my_resume \n4) /info", chat_id=message.from_user.id)


@dp.message_handler(commands="info")
async def info(message: types.Message):
    await bot.send_message(text="Ой як впадлу мені це писать мені це писать мені мені це писать", chat_id=message.from_user.id)


@dp.message_handler(commands="do_my_resume")
async def resume(message: types.Message):
    global saved_message, saved_message1, saved_message2
    await bot.send_message(text="Ля-ля-ля", chat_id=message.from_user.id, reply_markup=kb_resume)

#перший клас машина станів
class Form(StatesGroup):
    waiting_for_pib = State()

@dp.callback_query_handler(lambda c: c.data == 'PIB')
async def process_callback_pib(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введите ваше Прізвище Ім'я По-батькові:")
    await Form.waiting_for_pib.set()

@dp.message_handler(state=Form.waiting_for_pib)
async def process_pib(message: types.Message, state: FSMContext):
    global pib
    async with state.proxy() as data:
        pib = message.text

    await message.reply("Спасибо за информацию!")
    await state.finish()

@dp.message_handler(commands=['get_pib'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if pib:
            await message.reply(f"Ваше Прізвище Ім'я По-батькові: {pib}")
        else:
            await message.reply("Вы еще не ввели Прізвище Ім'я По-батькові.")

class Form1(StatesGroup):
    waiting_for_birthdaydate = State()

@dp.callback_query_handler(lambda c: c.data == 'birthdate')
async def process_callback_birthdaydate(message: types.Message, state: FSMContext,):
    await bot.send_message(message.from_user.id, text="Введіть вашу дату народження xx:xx:xxxx (число, місяць, рік):")
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
        print("Дата рождения соответствует формату и допустимым значениям.")
        await message.reply("Данні збережено")
    else:
        await message.reply("Дата рождения не соответствует формату или содержит недопустимые значения.")

    await state.finish()


@dp.message_handler(commands=['get_birthdate'])
async def get_birthdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if birthdate:
            await message.reply(f"Ваша дата народження: {birthdate}")
        else:
            await message.reply("Вы еще не ввели дату народження.")

class Form2(StatesGroup):
    waiting_for_adress = State()

@dp.callback_query_handler(lambda c: c.data == 'adress')
async def process_callback_adress(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть вашу адресу:")
    await Form2.waiting_for_adress.set()

@dp.message_handler(state=Form2.waiting_for_adress)
async def process_adress(message: types.Message, state: FSMContext):
    global address
    async with state.proxy() as data:
        address = message.text

    await message.reply("Інформацію збережено")
    await state.finish()

@dp.message_handler(commands=['get_adress'])
async def get_adress(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if address:
            await message.reply(f"Ваша адреса: {address}")
        else:
            await message.reply("Вы еще не ввели адресу.")

class Form3(StatesGroup):
    waiting_for_phonenum = State()


def check_phone_format(phone):
    pattern = "/^\+380\d{3}\d{2}\d{2}\d{2}$/"
    if re.match(pattern, phone.replace(" ", "")):
        return True
    return False

@dp.callback_query_handler(lambda c: c.data == 'phone_num')
async def process_callback_pib(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введите ваш номер телефону:")
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
                print(f"Номер '{number}' соответствует допустимому формату.")
                await message.reply("Номер збереженно")
            else:
                print(f"Номер '{number}' не соответствует допустимому формату.")
                phone_num = ""

        if phone_num == "":
            await message.reply("Номер введено неправильно")
        else:
            pass

        # for number in phone_numbers:
        #     if check_phone_format(number):
        #         print(f"Номер '{number}' соответствует допустимому формату.")
        #         await message.reply("Інформацію збережено")
        #         break
        #     else:
        #         print(f"Номер '{number}' не соответствует допустимому формату.")
        #         phone_num = ""
        # if phone_num == "":
        #     await message.reply("Номер введено неправильно")
        # else:
        #     pass

        await state.finish()

@dp.message_handler(commands=['get_phone_num'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if phone_num:
            await message.reply(f"Ваш номер телефону: {phone_num}")
        else:
            await message.reply("Вы еще не ввели номера телефону.")

class Form4(StatesGroup):
    waiting_for_comm = State()

@dp.callback_query_handler(lambda c: c.data == 'communication')
async def process_callback_communication(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть інші способи комунікації:")
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

def check_email_format(email):
    # Паттерн для проверки формата email адреса
    pattern = r"^[a-zA-Z0-9._%+-]+@(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3})$"
    if re.match(pattern, email):
        return True
    return False

def check_allowed_domain(email, allowed_domains):
    domain = email.split('@')[-1]
    return domain in allowed_domains

# Список разрешенных доменов
allowed_domains = [
    "gmail.com",
    "yahoo.com",
    "microsoft.com",
    "i.ua",
    "ukrnet.com",
    "meta.ua",
]

# Примеры email адресов
email_addresses = [
    "user@gmail.com",
    "user123@yahoo.com",
    "user.mail@microsoft.com",
    "user@i.ua",
    "user@ukrnet.com",
    "user@meta.ua"
]


@dp.callback_query_handler(lambda c: c.data == 'email')
async def process_callback_communication(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть інші способи комунікації:")
    await Form5.waiting_for_email.set()

@dp.message_handler(state=Form5.waiting_for_email)
async def process_communication(message: types.Message, state: FSMContext):
    global email
    async with state.proxy() as data:
        email = message.text

    for email in email_addresses:
        if email.endswith("@") and check_email_format(email[:-1]) and check_allowed_domain(email[:-1], allowed_domains):
            print(f"Email '{email}' соответствует допустимому формату и имеет разрешенный домен.")
            await message.reply("Інформацію збережено")
            break
        else:
            print(f"Email '{email}' не соответствует допустимому формату или не имеет разрешенный домен.")
            email = ""

        if email == "":
            await message.reply("емейл введено неправилно")
            break
        else:
            pass
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

@dp.callback_query_handler(lambda c: c.data == 'osvita')
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
    await bot.send_message(message.from_user.id, text="Яка у вас освіта:", reply_markup=keyboard)
    await Form6.waiting_for_osvita.set()

# Добавьте обработку callback'ов для каждого варианта образования
# Например:
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

@dp.message_handler(commands=['get_osvita'])
async def get_osvita(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global osvita
        if osvita:
            await message.reply(f"Ви вибрали: {osvita}")
        else:
            await message.reply("Вы еще не вибрали вашу освіту.")

class Form7(StatesGroup):
    waiting_for_add = State()

@dp.callback_query_handler(lambda c: c.data == 'add')
async def process_callback_add(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Бажаете щось додати?:")
    await Form7.waiting_for_add.set()

@dp.message_handler(state=Form7.waiting_for_add)
async def process_pib(message: types.Message, state: FSMContext):
    global add
    async with state.proxy() as data:
        add = message.text

    await message.reply("Інформацію збережено!")
    await state.finish()

@dp.message_handler(commands=['get_adding'])
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


@dp.message_handler(commands=['send_anketa'])
async def send_photo_to_admin(message: types.Message):
    admin_user_id = '1172984681'  # Замените на ID администратора
    photo_path = 'anketa.png'  # Путь к вашей фотографии

    # Отправка фотографии администратору
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(chat_id=admin_user_id, photo=photo, caption="Ваша фотография")



async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

executor.start_polling(dp, on_startup=on_startup, skip_updates=True)