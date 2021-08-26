"""
OpenWeather
API
key: bac78fa327b6bb2e8fa4f3a409a15252

"""
import requests
from requests.models import Response
from data import config
from datetime import datetime
s_city = 'Kiev'


WEATHER_LINK = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}'
GEO_LINK = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}'


def get_cords(city_name):
    link = GEO_LINK.format(city_name, config.API_KEY)
    r = requests.get(link)
    errors = r.json()
    try:

        if errors['cod'] == '404':
            return None
    except Exception as ex:
        print(ex)

    res = []
    for el in r.json():
        res.append({'name': el['name'], 'lon': el['lon'], 'lat': el['lat'], 'country': el['country']})
    return res


def get_weather(lat:str, lon:str, exclude= '',  lan='eng'):
    link = WEATHER_LINK.format(lat, lon, exclude, config.API_KEY)
    print(link)
    r = requests.get(link)
    return r.json()


def detailed_48_hours(text, delay=2):
    res = ''
    hour = datetime.now().hour
    '''
    for el in text:
        s = "{} o'clock: {} °C, {}, {} chance of rain".format(hour, int(el['temp'] - 272.15), el['weather'][0]['main'], el['pop'])
        s += '\n'
        hour += 1
        if hour == 24:
            hour = 0
        res += s
    '''

    for i in range(0, len(text), delay):
        s = "{}:00 {} °C, {}, {} chance of rain".format(hour, int(text[i]['temp'] - 272.15), text[i]['weather'][0]['main'],
                                                              text[i]['pop'])
        s += '\n'
        hour += delay
        if hour >= 24:
            hour -= 24
        res += s
    return res


def week_forecast(text):
    res = ''
    date = datetime.now().day
    for el in text:
        s = f'{date}) min: {int(el["temp"]["min"] - 272.15)} max:{int(el["temp"]["max"] - 272.15)}, {el["weather"][0]["description"]}, ' \
            f'chance of rain(snow): {el["pop"]}'
        s += '\n'
        date += 1
        res += s
    return res


def send_weather(mode, lat, lon):
    if mode == 'Today':
        return None

    elif mode == 'Tomorrow':
        return None

    elif mode == '2 days, detailed':
        weather_data = get_weather(lat, lon)['hourly']
        return detailed_48_hours(weather_data)

    elif mode == '7 days':
        weather_data = get_weather(lat, lon)['daily']

        return week_forecast(weather_data)


def find_city_in_massage(s):
    return s[0:s.index(' ')]

