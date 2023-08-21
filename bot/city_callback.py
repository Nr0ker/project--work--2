from aiogram import types
from bot.data.config import dp, bot
from keyboards import kb_rayon
from aiogram.dispatcher import FSMContext
from statesfile import StepStates


@dp.callback_query_handler(text="Kyiv_callback", state=StepStates.sity)
async def Work_in_Kiev(message: types.Message):
    await bot.send_message(text="Тепер, виберіть район", chat_id=message.from_user.id, reply_markup=kb_rayon)
    await StepStates.next()





@dp.callback_query_handler(text="dnypro_callback")

@dp.callback_query_handler(text="charkiv_callback")

@dp.callback_query_handler(text="zapori_callback")

@dp.callback_query_handler(text="odesa_callback")

@dp.callback_query_handler(text="lviv_callback")

@dp.callback_query_handler(text="all_callback")
