from aiogram import types

kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text='Київ', callback_data='Kyiv_callback')]
    ]
)
