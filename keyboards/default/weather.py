from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

weather_time = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Today'),
        KeyboardButton(text='Tomorrow')
    ],
    [
        KeyboardButton(text='5 days'),
        KeyboardButton(text='10 days')
    ],
    [
        KeyboardButton(text='Change city'),
    ]
], resize_keyboard=True)