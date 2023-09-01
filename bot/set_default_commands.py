from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("help", "Отримати допомогу"),
            types.BotCommand("send_anketa", "Надіслати анкету"),
            types.BotCommand("confirm", "Зробити анкету"),
            types.BotCommand("do_my_resume", "Почати робити резюме"),
            types.BotCommand("info", "Інформація про бота"),
            types.BotCommand("", "Дізнатися ФІО"),
            types.BotCommand("info", "Інформація про бота"),
            types.BotCommand("info", "Інформація про бота"),
            types.BotCommand("info", "Інформація про бота"),
            types.BotCommand("info", "Інформація про бота"),
            types.BotCommand("info", "Інформація про бота"),

        ]
    )
