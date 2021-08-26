from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

weather_time = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Today'),
        KeyboardButton(text='Tomorrow')
    ],
    [
        KeyboardButton(text='2 days, detailed'),
        KeyboardButton(text='7 days')
    ],
    [
        KeyboardButton(text='Send my location', request_location= True),
    ]
], resize_keyboard=True)

city_choose_keyboard = ReplyKeyboardMarkup(keyboard=
                                    [
                                        [KeyboardButton(text= 'Kiev')],
                                        [KeyboardButton(text= 'Lviv')],
                                        [KeyboardButton(text= 'Send location', request_location=True)]
                                    ], resize_keyboard= True)


async def create_city_keyboard(cities:dict, mode='create_1'):
    boards = []
    if cities:
        for el in range(len(cities)):
            if mode == 'create_2':
                name_board = KeyboardButton(text='{}) {}, {}'.format(el+1, cities[el]['name'], cities[el]['country']))
            else:
                name_board = KeyboardButton(text='{} {}'.format(cities[el]['name'], cities[el]['country']))
            boards.append([name_board])

    boards.append([KeyboardButton('Send location', request_location=True)])
    City_keyboard = ReplyKeyboardMarkup(keyboard=boards, resize_keyboard=True)

    return City_keyboard

