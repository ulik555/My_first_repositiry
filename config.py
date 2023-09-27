from pyowm.owm import OWM
import requests as req
import time

TOKEN = 'token bota'  # token bota
KEY = 'api key weather'  # api key


def get_valute() -> str:
    """Данная функция собирает данные о курсе валют с сайта,
     и возращает курс доллара и евро"""
    data = req.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    # time.ctime выводить дату и время
    exchange_rate = f'''{time.ctime()}
$ ->  {round(data["Valute"]["USD"]["Value"], 1)} руб
€ ->  {round(data["Valute"]["EUR"]["Value"], 1)} руб'''
    return exchange_rate


def get_weather(city):
    '''Данная функция принимает 1 параметр, название города.
    И выводит температуру и скорость ветра'''
    owm = OWM(KEY)  # api key
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place(city).weather
    temper = weather.temperature('celsius')  # возращает словарь с температурой
    temp = {k: v for k, v in temper.items()if k == 'temp' or k == 'feels_like'}
    t_today = round(temp["temp"], 1)  # температура воздуха
    feels = round(temp["feels_like"], 1)  # t° ощущается как

    observation = mgr.weather_at_place(city)  # ветер
    speed_wind = observation.weather.wind()  # возращает скор. ветра
    sp_wind = round(speed_wind['speed'], 1)  # округление скорости ветра

    return f'''Погода в {city}: Температура: {t_today}°С
ощущается как {feels}℃
    \nСкорость ветра: {sp_wind} м/c'''


# print(get_weather('London'))
