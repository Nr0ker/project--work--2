from aiogram import types, Bot
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_resume = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text="Прізвище, Ім`я, По-батькові", callback_data='LFM_name')],
        [types.InlineKeyboardButton(text="Фах", callback_data='work_callback')],
        [types.InlineKeyboardButton(text="Дата народження", callback_data='birthdate')],
        [types.InlineKeyboardButton(text="Номер телефону", callback_data='phone_num')],
        [types.InlineKeyboardButton(text="Електронна адреса", callback_data='email')],
        [types.InlineKeyboardButton(text="Освіта", callback_data='education')],
        [types.InlineKeyboardButton(text="Досвід", callback_data='exp_callback')]

    ]
)

kb_work = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text="Senior розробник ПО", callback_data='senoir_callabck')],
        [types.InlineKeyboardButton(text="Маркетинговий Менеджер", callback_data='marketing_callback')],
        [types.InlineKeyboardButton(text="Тех. підтримка", callback_data='tech_callback')],
        [types.InlineKeyboardButton(text="Frontend розробник", callback_data='front_callback')],
        [types.InlineKeyboardButton(text="Backend розробник(python)", callback_data='back_callback')],
        [types.InlineKeyboardButton(text="DevOps інженер", callback_data='devops_callback')],
        [types.InlineKeyboardButton(text="Data Scientist", callback_data='dataS_callback')],
        [types.InlineKeyboardButton(text="Системний адміністратор.", callback_data='sysAdmin_callback')]
    ]
)


kb_yes_no = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text="Прийняти", callback_data='apply_callback')],
        [types.InlineKeyboardButton(text="Відхилити", callback_data='reject_callback')]

    ]
)

