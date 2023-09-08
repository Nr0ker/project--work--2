from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("help", "Отримати допомогу"),
            types.BotCommand("info", "Інформація про бота"),
            types.BotCommand("send_survey", "Надіслати анкету"),
            types.BotCommand("confirm", "Зробити анкету"),
            types.BotCommand("get_date_of_birth", "Отримати дату народження"),
            types.BotCommand("get_phone_num", "Ваш номер телефону"),
            types.BotCommand("get_email", "Ваш E-mail"),
            types.BotCommand("get_education", "Ваше освіта"),
            types.BotCommand("get_exp", "Ваш досвід роботи")

        ]
    )







