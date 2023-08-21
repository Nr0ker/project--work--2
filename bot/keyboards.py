from aiogram import types

kb_cities = types.InlineKeyboardMarkup(
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

kb_rayon = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=' Голосіївський ', callback_data='golos_callback')],
        [types.InlineKeyboardButton(text='Дарницький', callback_data='darn_callback')],
        [types.InlineKeyboardButton(text='Деснянський', callback_data='desn_callback')],
        [types.InlineKeyboardButton(text='Дніпровський', callback_data='dnipro_callback')],
        [types.InlineKeyboardButton(text='Оболонський', callback_data='obolon_callback')],
        [types.InlineKeyboardButton(text='Печерський', callback_data='pechersk_callback')],
        [types.InlineKeyboardButton(text='Подільський', callback_data='podil_callback')],
        [types.InlineKeyboardButton(text='Святошинський', callback_data='svyatosh_callback')],
        [types.InlineKeyboardButton(text="Солом'янський", callback_data='solom_callback')],
        [types.InlineKeyboardButton(text='Шевченківський', callback_data='shevch_callback')]

    ]
)
