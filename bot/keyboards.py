from aiogram import types

kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text='Київ', callback_data='Kyiv_callback')],
        [types.InlineKeyboardButton(text='Дніпро', callback_data='dnypro_callback')],
        [types.InlineKeyboardButton(text='Харків', callback_data='charkiv_callback')],
        [types.InlineKeyboardButton(text='Запоріжжя', callback_data='zapori_callback')],
        [types.InlineKeyboardButton(text='Одеса', callback_data='odesa_callback')],
        [types.InlineKeyboardButton(text='Львів', callback_data='lviv_callback')],
        [types.InlineKeyboardButton(text='Пошук по всій Україні', callback_data='all_callback')]

    ]
)
