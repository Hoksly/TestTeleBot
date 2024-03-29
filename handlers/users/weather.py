from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import ReplyKeyboardRemove
from keyboards.default import weather_time, create_city_keyboard
from loader import dp
from states.weather import Weather
from aiogram.dispatcher import FSMContext
from utils.misc.send_weather import get_cords, send_weather, find_city_in_massage
from string import digits
from data.database.weather_databse.weather_db import get_users_cities, check_user, find_city
'''
@dp.message_handler(Command('menu'))
async def bot_start(message: types.Message):
    await message.answer("Bot is working, for now.")
'''
YES = ['yes', 'Yes', 'YES', 'yES', 'yEs', 'YeS']
NO = ['NO', 'no', 'No', 'nO']


@dp.message_handler(Command('weather'), state='*')
async def ask_city(message: types.Message):
    cities = await get_users_cities(message.from_user.id)
    k_b = await create_city_keyboard(cities, mode='create_1')
    await message.answer("Your city name?", reply_markup=k_b)
    await Weather.Get_city_name.set()


@dp.message_handler(state=Weather.Get_city_name)
async def get_city_name(message: types.Message, state: FSMContext):
    if message.location:
        print('message.location:')
        print(message.location)
        location = message.location
        await state.update_data(location=location)
    else:
        city_name = find_city_in_massage(message.text)
        c_lat, c_lon, c_name, c_country, c_id = find_city(message.text)
        if not c_lat:
            cities = get_cords(city_name)
            if not cities:
                await message.answer('Could not find this city. Is name of it correct? \nRemember, that you can send your location directly')
                return 0
            await state.update_data(cities=cities)

            if len(cities) > 1:
                cities_keyboard = create_city_keyboard(cities, mode='create_2')
                await message.answer('Here is some cities with same name, in what do you interested?', reply_markup=await cities_keyboard)
                await Weather.Choose_city.set()

            else:
                await state.update_data({'lat': cities[0]['lat'], 'lon': cities[0]['lon'],
                                         'name': cities[0]['name'], 'country': cities[0]['country']})
                await message.answer('Forecast duration?', reply_markup=weather_time)
                await Weather.Choose_duration.set()
        else:
            await state.update_data({'lat': c_lat, 'lon': c_lon,
                                     'name': c_name, 'country': c_country})
            await message.answer('Forecast duration?', reply_markup=weather_time)
            await Weather.Choose_duration.set()


@dp.message_handler(state=Weather.Choose_city)
async def choose_city(message: types.Message, state: FSMContext):
    number = message.text[0]
    if number not in digits:
        await message.answer('Choose city from a keyboard')
    else:
        s_data = await state.get_data()
        cities = s_data.get('cities')
        await state.update_data({'lat': cities[int(number) - 1]['lat'], 'lon': cities[int(number) - 1]['lon'],
                                 'name': cities[int(number) - 1]['name'], 'country': cities[int(number) - 1]['country']})
        await message.answer('Forecast duration?', reply_markup=weather_time)
        await Weather.Choose_duration.set()


@dp.message_handler(state= Weather.Choose_duration)
async def choose_duration(message: types.Message, state: FSMContext):
    all_data = await state.get_data()

    duration = message.text
    lat = all_data.get('lat')
    lon = all_data.get('lon')
    c_id = await check_user(message.from_user.id, all_data.get('name'), all_data.get('country'), lat, lon)
    if duration == 'Today':
        await message.answer('This function is not released yet')

    elif duration == 'Tomorrow':
        await message.answer('This function is not released yet')

    elif duration == '2 days, detailed':
        answer = send_weather('2 days, detailed', lat, lon, c_id=c_id)
        await message.answer(answer, reply_markup=ReplyKeyboardRemove())
        await state.reset_state(with_data=True)
    elif duration == '7 days':
        answer = send_weather('7 days', lat, lon, c_id=c_id)
        await message.answer(answer, reply_markup=ReplyKeyboardRemove())
        await state.reset_state(with_data=True)
    else:
        await message.answer('Choose the duration from keyboard')
        return 0


'''

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

'''