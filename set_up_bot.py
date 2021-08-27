import os
import sqlite3
from data.config import WEATHER_FORECAST_FOLDER, WEATHER_DB_ADDRES
from data.database.weather_databse.weather_db import recreate_db

def create_dir(folder_path):
    try:
        os.mkdir(folder_path)
    except:
        pass


def create_db(db_path):
    sqlite3.connect(db_path)


create_dir('data/database/weather_databse/db')
create_dir(WEATHER_FORECAST_FOLDER)
create_db(WEATHER_DB_ADDRES)
recreate_db()