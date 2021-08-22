from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
AAPID = env.str("AAPID")
WEATHER_ADRES = env.str("WEATHER_ADRES")
API_KEY = env.str("WEATHER_API_KEY")
UNIX_YEAR = env.int('UNIX_YEAR')
UNIX_MONTH = env.int('UNIX_MONTH')
UNIX_WEEK = env.int('UNIX_WEEK')
UNIX_DAY = env.int('UNIX_DAY')
WEATHER_DB_ADDRES = env.str('WEATHER_DB')
