import json
import sqlite3
from loader import db
from time import time

from data.config import WEATHER_FORECAST_FOLDER
import os
import requests
from data import config
from datetime import datetime, timedelta

sql = db.cursor()

WEATHER_LINK = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}'


def recreate_db():
    sql.execute("""CREATE TABLE IF NOT EXISTS city (
            id INT PRIMARY KEY, 
            name TEXT, 
            country TEXT,
            forecast_cur_updated TEXT,
            forecast_2d_updated TEXT,
            forecast_7d_updated TEXT,
            forecast_30d_updated TEXT,
            lat REAL,
            lon REAL

            )""")
    sql.execute(""" CREATE TABLE IF NOT EXISTS user(
                id INT PRIMARY KEY,
                send_alerts INT,
                send_daily INT)
    """)

    sql.execute("""
        CREATE TABLE IF NOT EXISTS 'interested_in' (
	    'user_id'	INTEGER NOT NULL,
	    'city_id'	INTEGER NOT NULL,
	    FOREIGN KEY('user_id') REFERENCES "user"('id'),
	    PRIMARY KEY('user_id','city_id'))

        """)


def get_weather_folder(city, country):
    return WEATHER_FORECAST_FOLDER + '/' + city + '_' + country


"""
Structure: forecast_folder/city_folder
In this folder will be second files:
forecast_minutely.json
forecast_hourly.json
forecast_daily.json
forecast_monthly.json


"""


def create_folder(path):
    try:
        os.mkdir(path)
    except:
        print("This folder already exist:", path)


def create_weather_files(folder):
    open(folder + '/forecast_minutely.json', 'w')
    open(folder + '/forecast_hourly.json', 'w')
    open(folder + '/forecast_daily.json', 'w')
    open(folder + '/forecast_monthly.json', 'w')


def get_city(city_id):
    sql.execute("""
    SELECT name, country FROM city WHERE id = '{}'
    """.format(city_id))
    ret = sql.fetchone()
    return {'name': ret[0], 'country': ret[1]}


async def get_users_cities(user_id):
    sql.execute("""
    SELECT city_id from interested_in WHERE user_id = '{}'
    """.format(user_id))
    c_data = sql.fetchall()
    if c_data:
        ret = []
        for el in c_data[:5]:
            ret.append(get_city(el[0]))
        return ret

        pass
    else:
        return None


def add_city_to_user(user_id, city_id):
    sql.execute("""
            INSERT INTO interested_in VALUES (?,?)""", (user_id, city_id))

    db.commit()


def check_city_to_user_connection(user_id, city_id):
    sql.execute("""
    SELECT * FROM interested_in WHERE user_id = ? AND city_id = ?
    """, (user_id, city_id))
    return bool(sql.fetchone())


def add_user(user_id, send_alerts=False, send_daily=False):
    sql.execute("""
       INSERT INTO user VALUES (?, ?, ?)""", (int(user_id), int(send_alerts),
                                              int(send_daily)))
    db.commit()


async def check_user(user_id, city_name, city_country, city_lat, city_lon, send_alerts=False, send_daily=False):
    sql.execute("""
        SELECT * FROM user WHERE id = '{}'
    """.format(int(user_id)))
    resp = sql.fetchone()
    if not resp:
        add_user(user_id)

    city_id = check_city(city_name, city_country, city_lat, city_lon)
    if not check_city_to_user_connection(user_id, city_id):
        add_city_to_user(user_id, city_id)

    return city_id


def add_city(city_name, city_country, lat, lon,
             forecast_cur=None, forecast_2d=None, forecast_7d=None, forecast_30d=None,
             forecast_cur_updated=None, forecast_2d_updated=None, forecast_7d_updated=None, forecast_30d_updated=None):
    sql.execute("""
    SELECT id from city
    """)
    try:
        c_id = sql.fetchall()[-1]
    except IndexError:
        c_id = None

    if c_id is None:
        c_id = 1
    else:
        c_id = max(c_id) + 1
    sql.execute("""
    INSERT INTO city VALUES (?, ? , ?, ?, ?, ?, ?, ?, ?)
    """, (c_id, city_name, city_country, forecast_cur_updated, forecast_2d_updated,
          forecast_7d_updated, forecast_30d_updated, lat, lon))

    db.commit()
    os.mkdir(get_weather_folder(city_name, city_country))
    create_weather_files(get_weather_folder(city_name, city_country))

    return c_id


def check_city(city_name, city_country, city_lat, city_lon):
    sql.execute("""
    SELECT id from city WHERE name = ? AND country = ?
    """, (city_name, city_country))

    c_id = sql.fetchone()
    if c_id:
        return c_id[0]
    else:
        return add_city(city_name=city_name, city_country=city_country, lat=city_lat, lon=city_lon)


def find_city(message: str):
    try:
        name, country = message.split()
    except:
        return None, None, None, None, None
    sql.execute("""
    SELECT lat, lon, id FROM city WHERE name = '{}' AND country = '{}'
    """.format(name, country))
    res = sql.fetchone()
    if res:
        return res[0], res[1], name, country, res[2]
    else:
        return None, None, None, None, None


def check_time(mode, t_time):
    if not t_time[0]:
        return True

    if mode == 'cur':  # once per 5 minutes
        return (time() - int(t_time[0])) >= 5 * 60
    elif mode == '2d':  # once per hour
        return (time() - int(t_time[0])) >= 60 * 60
    elif mode == '7d':  # once per day
        return (time() - int(t_time[0])) >= 60 * 60 * 24


def write_changes_2d(json_data, file, city_id):
    json.dump(json_data, file)
    sql.execute("""
    UPDATE city SET forecast_2d_updated = '{}' WHERE id = '{}'
    """.format(int(time()), city_id))


def write_changes_7d(json_data, file, city_id):
    json.dump(json_data, file)
    sql.execute("""
    UPDATE city SET forecast_7d_updated = '{}' WHERE id = '{}'
    """.format(int(time()), city_id))


def write_changes_30d(json_data, file, city_id):
    json.dump(json_data, file)
    sql.execute("""
    UPDATE city SET forecast_30d_updated = '{}' WHERE id = '{}'
    """.format(int(time()), city_id))


def update_user_send_alerts(user_id):
    pass


def update_user_send_daily(user_id):
    pass


def update_forecast_current(city_id, forecast):
    pass


def give_forecast_2days(city_id):
    sql.execute("""
        SELECT forecast_2d_updated from city WHERE id = '{}'
        """.format(city_id))
    res = sql.fetchone()
    if check_time('2d', res):
        sql.execute("""
        SELECT lat, lon, country, name FROM city WHERE id = '{}'
        """.format(city_id))
        lat, lon, country, name = sql.fetchone()

        link = WEATHER_LINK.format(lat, lon, '',
                                   config.API_KEY)  # '' is for exclude - exclude nothing, give all weather
        r = requests.get(link)
        with open(get_weather_folder(name, country) + '/forecast_hourly.json', 'w') as file:
            write_changes_2d(r.json()['hourly'], file, city_id)

        return r.json()['hourly']
    else:
        sql.execute("""
                    SELECT country, name FROM city WHERE id = '{}'
                    """.format(city_id))
        country, name = sql.fetchone()

        with open(get_weather_folder(name, country) + '/forecast_hourly.json', 'r') as file:
            return json.load(file)


def give_forecast_week(city_id):
    sql.execute("""
            SELECT forecast_7d_updated from city WHERE id = '{}'
            """.format(city_id))
    if check_time('7d', sql.fetchone()):
        sql.execute("""
            SELECT lat, lon, country, name FROM city WHERE id = '{}'
            """.format(city_id))
        lat, lon, country, name = sql.fetchone()

        link = WEATHER_LINK.format(lat, lon, '',
                                   config.API_KEY)  # '' is for exclude - exclude nothing, give all weather
        r = requests.get(link)
        with open(get_weather_folder(name, country) + '/forecast_daily.json', 'w') as file:
            write_changes_2d(r.json()['daily'], file, city_id)

        return r.json()['daily']
    else:
        sql.execute("""
                    SELECT country, name FROM city WHERE id = '{}'
                    """.format(city_id))
        country, name = sql.fetchone()

        with open(get_weather_folder(name, country) + '/forecast_daily.json', 'r') as file:
            return json.load(file)


def update_forecast_month(city_id, forecast):
    pass


def update_city_forecast(weather):
    pass


def get_weather_db(city_id, mode):
    if mode == '2d':
        return give_forecast_2days(city_id)
    elif mode == '7d':
        return give_forecast_week(city_id)
