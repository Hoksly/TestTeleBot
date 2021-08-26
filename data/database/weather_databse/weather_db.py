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
        for el in c_data:

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


def add_city(city_name, city_country, lat, lon,
             forecast_cur=None, forecast_2d=None, forecast_7d=None, forecast_30d=None,
             forecast_cur_updated=None, forecast_2d_updated=None, forecast_7d_updated=None, forecast_30d_updated=None):
    sql.execute("""
    SELECT id from city
    """)
    c_id = sql.fetchall()[-1]
    if c_id is None:
        c_id = 1
    else:
        c_id = max(c_id) + 1
    sql.execute("""
    INSERT INTO city VALUES (?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (c_id, city_name, city_country, forecast_cur, forecast_2d, forecast_7d, forecast_30d,
          forecast_cur_updated, forecast_2d_updated, forecast_7d_updated, forecast_30d_updated, lat, lon))

    db.commit()
    return c_id


def check_city(city_name, city_country, city_lat, city_lon):
    sql.execute("""
    SELECT id from city WHERE name = ? AND country = ?
    """, (city_name, city_country))

    id = sql.fetchone()
    # print(type(id), id)
    if id:
        return id[0]
    else:
        return add_city(city_name=city_name, city_country=city_country, lat=city_lat, lon=city_lon)


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


get_city(1)
print(sql.fetchall())
