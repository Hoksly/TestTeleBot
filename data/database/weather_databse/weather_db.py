import sqlite3
from loader import db


sql = db.cursor()


def recreate_db():
    sql.execute("""CREATE TABLE IF NOT EXISTS city (
            id INT PRIMARY KEY, 
            name TEXT, 
            country TEXT,
            forecast_cur TEXT,
            forecast_2d TEXT,
            forecast_7d TEXT,
            forecast_30d, TEXT,
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


def add_user(user_id, send_alerts = False, send_daily= False):
    sql.execute("""
    INSERT INTO user VALUES (id, send_alerts, send_daily) (?, ?, ?)""",
                (user_id, int(send_alerts), int(send_daily)))


def check_city(city_name, city_country):
    city_id = ''

    return city_id


def update_user_send_alerts(user_id):
    pass


def update_user_send_daily(user_id):
    pass


def update_forecast_current(city_id, forecast):
    pass


def update_forecast_2days(city_id, forecast):
    pass


def update_forecast_week(city_id, forecast):
    pass


def update_forecast_month(city_id, forecast):
    pass

db.close()