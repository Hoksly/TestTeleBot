from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import menu
from aiogram.dispatcher.filters import Command, Text


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Chose the product below", reply_markup=menu)


@dp.message_handler(Text(equals=["Котлетки", 'Макарошки', "Пюрешка"]))
async def get_food(message: Message):
    await message.answer(f"You chose {message.text}. Thanks.", reply_markup=ReplyKeyboardRemove())