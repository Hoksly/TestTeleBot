from aiogram.dispatcher.filters.state import StatesGroup, State


class Weather(StatesGroup):
    Get_city_name = State()
    Get_cords = State()
    Choose_city = State()
    Choose_duration = State()
    Print_weather = State()


