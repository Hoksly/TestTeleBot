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

'''
try:
    result = requests.get('http://api.openweathermap.org/data/2.5/find', params={'q':s_city, 'type': 'like',
                                                                             "units":'metrics', 'APPID':appid })
    res = result.text
    data = result.json()
    # print(data)

    cities = ["{} ({})".format(d['name'], d['sys']['country'])
              for d in data['list']]
    # print("city:", cities)
    city_id = data['list'][0]['id']
    # print('city_id=', city_id)
    new = data['list']

    el1 = new[0]
    el2 = new[1]

except Exception as e:
    print(str(e))

'''
"""
def print_weather(t_min, t_max, t_feels, weather, snow, rain, city):
    print('city:', s_city)
    if snow:
        snow_time = list(snow.keys())[0]
        snow_pr = snow[snow_time]
        print('It will be snow in', snow_time)
        print('snow intensity:', snow_pr)
    else:
        print("It is not snowy today")

    if rain:
        rain_time = rain[0]
        rain_pr = rain[rain_time]
        print('It will be rain in', rain_time)
        print('rain intensity:', rain_pr)

    else:
        print('It is not rainy today')

    id, main, description, icon = weather['id'], weather['main'], weather['description'], weather['icon']
    print("Today's maximum temperature:", round(t_max - 273))
    print("Today's minimum temperature:", round(t_min - 273))
    print('It feels like:', round(t_feels - 273))
    print('weather id:', id)
    print('weather description:', description)


def get_weather(s_city = 'Kyiv', cloudy_metric = 0.1, android = True):

    a = requests.get('http://api.openweathermap.org/data/2.5/find', params={'q': s_city, 'type': 'like',
                                                                 "units": 'metrics', 'APPID': AAPID})
    data = a.json()
    result1 = data['list'][0]

    """
"""
# Another helpful data
result2 = data['list'][1]

for el in result1:
    print(el, result1[el])

for el in result2:
    print(el, result2[el])
"""
"""

    snow = bool(result1['snow'])
    rain = bool(result1['rain'])
    clouds = result1['clouds']['all']
    weather = result1['weather']

    main = result1['main']
    weather = result1['weather']

    rain = result1['rain']

    snow = result1['snow']


    temp_min = main['temp_min']
    temp_max = main['temp_max']
    feels_like = main['feels_like']

    if android:
        print_weather(temp_min, temp_max, feels_like, weather[0], snow, rain, s_city)

    return None


weather = get_weather(s_city)
if weather:
    print(weather)

"""

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
