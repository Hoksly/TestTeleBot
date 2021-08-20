from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp


@dp.message_handler(commands=['statement'])
async def bot_start(message: types.Message):
    await message.answer("Bot is working, for now.")

