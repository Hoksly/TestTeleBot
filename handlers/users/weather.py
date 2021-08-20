from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from keyboards.default import weather_time

from loader import dp
from states.weather import Weather
from aiogram.dispatcher import FSMContext

'''
@dp.message_handler(Command('menu'))
async def bot_start(message: types.Message):
    await message.answer("Bot is working, for now.")
'''
YES = ['yes', 'Yes', 'YES', 'yES', 'yEs', 'YeS']
NO = ['NO', 'no', 'No', 'nO']


@dp.message_handler(Command('weather'))
async def enter_test(message: types.Message):
    await message.answer('Started test. \nAre you ok?')

    await Weather.Q1.set()


@dp.message_handler(state= Weather.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)

    await message.answer('Question 2. \nAre you want to die?')

    await Weather.next()


@dp.message_handler(state= Weather.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    data = await state.get_data()
    answer1 = data.get('answer1')

    if answer1 in YES:
        if answer2 in NO:
            await message.answer('Ha-ha, nice joke \nhttps://vek-ritual.com.ua/ritualnye-tovary/groby-tkan/')
        elif answer2 in YES:
            await message.answer('Hey dude, I have a nice offer for you: \nhttps://vek-ritual.com.ua/ritualnye-tovary/groby-tkan/')
    else:
        if answer2 in NO:
            await message.answer('Am I joke to you?')
        else:
            await message.answer('Heeey, I have some offers, specially for you: \nhttps://vek-ritual.com.ua/ritualnye-tovary/groby-tkan/')

    await state.finish()