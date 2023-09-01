from aiogram import types

kb_resume = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text="Прізвище Ім`я По-батькові", callback_data='PIB')],
        [types.InlineKeyboardButton(text="Дата народження", callback_data='birthdate')],
        [types.InlineKeyboardButton(text="Адреса прописки", callback_data='adress')],
        [types.InlineKeyboardButton(text="Номер телефону", callback_data='phone_num')],
        [types.InlineKeyboardButton(text="Інші способи зв'язку", callback_data='communication')],
        [types.InlineKeyboardButton(text="Електронна адреса", callback_data='email')],
        [types.InlineKeyboardButton(text="Освіта", callback_data='osvita')],
        [types.InlineKeyboardButton(text="Додатково", callback_data='add')]
    ]
)