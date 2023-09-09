from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
from bot.data.config import dp, bot, ADMINS
from aiogram import types
from bot.keyboards import kb_resume, kb_yes_no, kb_work
from bot.__init__ import user_id

work = ""
pib = ""
exp = 0
birthdate = ""
phone_num = ""
email = ""
education = ""


class Form(StatesGroup):
    waiting_for_pib = State()


@dp.callback_query_handler(lambda c: c.data == 'LFM_name')
async def process_callback_pib(message: types.Message, state: FSMContext):
    global user_id
    user_id = message.from_user.id
    await bot.send_message(message.from_user.id, text="Введіть ваші прізвище, ім'я, по батькові: "
                                                      "Щоб подивитися, що ви ввели використайте /get_LFM_name")
    await Form.waiting_for_pib.set()


@dp.message_handler(state=Form.waiting_for_pib)
async def process_pib(message: types.Message, state: FSMContext):
    global pib
    async with state.proxy() as data:
        pib = message.text

    await message.reply("Збережено!")
    await state.reset_state()


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
async def process_callback_birthdaydate(message: types.Message, state: FSMContext, ):
    await bot.send_message(message.from_user.id,
                           text="Введіть вашу дату народження(вам повинно бути більше 18 років) по типу число, місяць, рік (наприклад 29 09 2003):"
                                "Щоб подивитися, що ви ввели використайте /get_date_of_birth")
    await Form1.waiting_for_birthdaydate.set()


def check_date_format(date):
    pattern = r'^(?:0[1-9]|[12][0-9]|3[01]) (?:0[1-9]|1[0-2]) (19[3-9][0-9]|200[0-3])$'
    match = re.match(pattern, date)
    if match:
        return True
    else:
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

        await state.reset_state()


@dp.message_handler(commands=['get_date_of_birth'])
async def get_birthdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if birthdate:
            await message.reply(f"Ваша дата народження: {birthdate}")
        else:
            await message.reply("Ви не ввели дату народження.")


class Form3(StatesGroup):
    waiting_for_phonenum = State()


def check_phone_format(phone):
    pattern = "^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    if re.match(pattern, phone.replace(" ", "")):
        return True
    return False


@dp.callback_query_handler(lambda c: c.data == 'phone_num')
async def process_callback_pib(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть ваш номер телефону"
                                                      "\n Щоб подивитися, що ви ввели використайте /get_phone_num")
    await Form3.waiting_for_phonenum.set()


@dp.message_handler(state=Form3.waiting_for_phonenum)
async def process_pib(message: types.Message, state: FSMContext):
    global phone_num
    async with state.proxy() as data:
        phone_num = message.text

        if check_phone_format(phone_num):
            print(f"Номер '{phone_num}' підходить.")
            await message.reply("Номер збереженно")
        else:
            print(f"Номер '{phone_num}' не підходить.")
            phone_num = ""

        if phone_num == "":
            await message.reply("Номер введено неправильно")
        else:
            pass

        await state.reset_state()


@dp.message_handler(commands=['get_phone_num'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if phone_num:
            await message.reply(f"Ваш номер телефону: {phone_num}")
        else:
            await message.reply("Ви ще не ввели номер телефону.")


class Form5(StatesGroup):
    waiting_for_email = State()


def check_email(email1):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b'
    email_list = re.findall(email_pattern, email1)

    for i in email_list:
        if not i.endswith('.ru'):
            return True

    return False


@dp.callback_query_handler(lambda c: c.data == 'email')
async def process_callback_communication(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Напишіть ваш E-mail"
                                                      "Щоб подивитися, що ви ввели використайте /get_email")
    await Form5.waiting_for_email.set()


@dp.message_handler(state=Form5.waiting_for_email)
async def process_communication(message: types.Message, state: FSMContext):
    global email
    async with state.proxy() as data:
        email = message.text
        if check_email(email):
            await message.reply("Інформацію збережено")
        else:
            await message.reply("Ви введи E-mail не правильно, або ви росіянин)")

        await state.reset_state()


@dp.message_handler(commands=['get_email'])
async def get_pib(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if email:
            await message.reply(f"Ваш E-mail: {email}")
        else:
            await message.reply("Ви еще не ввели ваш E-mail")


class ExpStatesGruop(StatesGroup):
    experience = State()


@dp.callback_query_handler(lambda c: c.data == 'exp_callback')
async def process_exp_callback(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text="Введіть ваш досвід роботи в вашій галузі(просто цифрою)"
                                                      "\nЩоб подивитися, що ви ввели, використайте /get_exp")
    await ExpStatesGruop.experience.set()


@dp.message_handler(state=ExpStatesGruop.experience)
async def process_exp(message: types.Message, state: FSMContext):
    global exp
    async with state.proxy() as data:
        exp = message.text
        if exp.isdigit():
            await message.reply("Досвід збережено.")
        else:
            await message.reply("Ви ввели щось не так, спробуйте ще раз.")

        await state.reset_state()


@dp.message_handler(commands=['get_exp'])
async def get_exp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if exp:
            await message.reply(f"Ваш досвід: {exp}")
        else:
            await message.reply("Ви ще не ввели ваш досвід.")


class Form6(StatesGroup):
    waiting_for_osvita = State()


class WorkGruopStates(StatesGroup):
    work = State()


@dp.callback_query_handler(lambda c: c.data == 'work_callback')
async def work_chose(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text="Виберіть посаду на якій ви хочете працювати: ",
                           reply_markup=kb_work)
    await WorkGruopStates.work.set()


@dp.callback_query_handler(lambda c: c.data == 'senoir_callabck', state=WorkGruopStates.work)
async def process_apply_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали senior розробника")
    global work
    async with state.proxy() as data:
        work = "Senior розробник"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'marketing_callback', state=WorkGruopStates.work)
async def process_marketing_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали Маркетинговий Менеджер")
    global work
    async with state.proxy() as data:
        work = "Маркетинговий Менеджер"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'tech_callback', state=WorkGruopStates.work)
async def process_tech_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали Тех. підтримка")
    global work
    async with state.proxy() as data:
        work = "Тех. підтримка"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'front_callback', state=WorkGruopStates.work)
async def process_front_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали Frontend розробника")
    global work
    async with state.proxy() as data:
        work = "Frontend розробник"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'back_callback', state=WorkGruopStates.work)
async def process_back_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали Backend розробника (Python)")
    global work
    async with state.proxy() as data:
        work = "Backend розробник (Python)"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'devops_callback', state=WorkGruopStates.work)
async def process_devops_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали DevOps інженера")
    global work
    async with state.proxy() as data:
        work = "DevOps інженер"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'dataS_callback', state=WorkGruopStates.work)
async def process_dataS_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали Data Scientist")
    global work
    async with state.proxy() as data:
        work = "Data Scientist"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'sysAdmin_callback', state=WorkGruopStates.work)
async def process_sysAdmin_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали Системного адміна.")
    global work
    async with state.proxy() as data:
        work = "Системний адміністратор"
        await state.reset_state()


@dp.message_handler(commands=['get_work'])
async def get_osvita(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global work
        if work:
            await message.reply(f"Ви вибрали: {work}")
        else:
            await message.reply("Ви ще не вибрали посаду")


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
                                                      "Щоб подивитися, що ви ввели використайте /get_education",
                           reply_markup=keyboard)
    await Form6.waiting_for_osvita.set()


@dp.callback_query_handler(lambda c: c.data == 'education_primary', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Ви вибрали 'Початкова загальна освіта'")
    global education
    async with state.proxy() as data:
        education = "Початкова загальна освіта"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'education_basic_secondary', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Базова загальна середня освіта'")
    global education
    async with state.proxy() as data:
        education = "Базова загальна середня освіта"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'education_full_secondary', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Повна загальна середня освіта")
    global education
    async with state.proxy() as data:
        education = "Повна загальна середня освіта"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'education_professional_technical', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Професійно-технічна освіта")
    global education
    async with state.proxy() as data:
        education = "Професійно-технічна освіта"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'education_incomplete_higher', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Неповна вища освіта")
    global education
    async with state.proxy() as data:
        education = "Неповна вища освіта"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'education_basic_higher', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Базова вища освіта")
    global education
    async with state.proxy() as data:
        education = "Базова вища освіта"
        await state.reset_state()


@dp.callback_query_handler(lambda c: c.data == 'education_full_higher', state=Form6.waiting_for_osvita)
async def process_education_primary(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, text="Повна вища освіта")
    global education
    async with state.proxy() as data:
        education = "Повна вища освіта"
        await state.reset_state()


@dp.message_handler(commands=['get_education'])
async def get_osvita(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global education
        if education:
            await message.reply(f"Ви вибрали: {education}")
        else:
            await message.reply("Вы еще не вибрали вашу освіту.")


def convert_date_format(date):
    try:
        date_obj = datetime.strptime(date, "%d:%m:%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None


@dp.message_handler(commands=['confirm'])
async def confirm_resume(message: types.Message):
    global user_id, pib, work, birthdate, phone_num, email, education, exp

    if pib != "" and work != "" and birthdate != "" and phone_num != "" and email != "" and education != "" and exp != "":
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project--2"
        )

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO resumes (user_id, pib, birthdate, phone_num, email, education, work, exp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, pib, birthdate, phone_num, email, education, work, exp))

        db.commit()
        cursor.close()
        db.close()

        await message.reply("Ваше резюме було збережено в базі данних!")

        width, height = 900, 600
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)

        image = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("arial.ttf", 40)

        x, y = 50, 50
        line_height = 40

        data = [
            "            Анкета",
            " ",
            f"ФИО: {pib}",
            f"Фах: {work}",
            f"Досвід роботи {exp}",
            f"Дата народження: {birthdate}",
            f"Телефон: {phone_num}",
            f"Email: {email}"
        ]

        for item in data:
            draw.text((x, y), item, fill=text_color, font=font)
            y += line_height

        image.save("anketa.png")

        photo_path = 'anketa.png'

        with open(photo_path, 'rb') as photo:
            await bot.send_photo(message.chat.id, types.InputFile(photo))

        work = ""
        user_id = ""
        pib = ""
        exp = ""
        birthdate = ""
        phone_num = ""
        email = ""
        education = ""

    else:
        await bot.send_message(chat_id=user_id, text="Ви заповнили не всі данні, спробуте ще раз!")
