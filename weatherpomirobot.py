import psycopg2
import requests
import datetime
from config import open_weather_token
from aiogram import types, Dispatcher
from aiogram.utils import executor
from create_bot import dp, bot
from handlers import weather, base
from handlers.scheduler import ScheduleMessage
from config import db_name, db_user, db_password, db_host, db_port
from psycopg2 import OperationalError
import time
import schedule
from multiprocessing.context import Process

connection = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    sslmode='require')


@dp.message_handler(lambda message: 'Погода каждое утро' in message.text)
async def get_city(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите название города")

def get_weather(city):
    print(1)
    # Библиотека смйлов
    code_to_smile = {
        "Clear": "☀ Ясно",
        "Clouds": "☁ Облачно",
        "Rain": "☔ Дождь",
        "Drizzle": "☔ Дождь",
        "Thunderstorm": "⛈ Гроза",
        "Snow": "❄ Снег",
        "Mist": "🌫 Туман"
    }
    # Отправка запроса на сервер для получения координат города
    loc = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={open_weather_token}"
    )
    loc = loc.json()

    lat = loc[0]['lat']
    lon = loc[0]['lon']

    r = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily'
        f'&appid={open_weather_token}&units=metric&lang=ru'
    )
    data = r.json()
    final = ""
    for i in range(16):
        dtime = datetime.datetime.fromtimestamp(data['hourly'][i]['dt'])
        time = dtime.strftime('%H:%M')
        desc = data['hourly'][i]['weather'][0]['main']
        try:
            desc_emoji = code_to_smile[desc]
        except:
            desc_emoji = desc
        temp = round(data['hourly'][i]['temp'])
        humidity = data['hourly'][i]['humidity']
        wind = round(data['hourly'][i]['wind_speed'])
        text = str(f'{time} {desc_emoji} 🌡 {temp}°C 💧{humidity}% 💨 {wind}м/с\n')
        final = final + text
    return final

def morning_push():
    print(2)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, city from morning_weather")
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0],
        city = row[1],
    text = get_weather(city)
    cursor.close()
    return [user_id, text]

@dp.message_handler()
async def get_query(message: types.Message):
    print(3)
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO morning_weather VALUES (%s, %s)", (message.from_user.id, message.text))
    except:
        cursor.execute("UPDATE morning_weather set city = (%s) where user_id = (%s)",
                       (message.text, message.from_user.id))
    connection.commit()
    cursor.close()
    data = morning_push()
    chat_id = str(data[0][0])
    text = str(data[1])
    await bot.send_message(chat_id=chat_id, text=text)


# def job():
#     print('test')


# schedule.every().day.at("08:00").do(morning_push)
# schedule.every(3).minutes.do(morning_push)
#
#
# class ScheduleMessage():
#     def try_send_schedule():
#         while True:
#             schedule.run_pending()
#             time.sleep(1)
#
#     def start_process():
#         p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
#         p1.start()


async def on_startup(_):
    print('Bot online')


async def on_shutdown(_):
    print('Bot offline')
    connection.close()


# def register_handlers_weather(dp: Dispatcher):
#     dp.register_message_handler(get_city, lambda message: 'Погода каждое утро' in message.text)

if __name__ == '__main__':
    # ScheduleMessage.start_process()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
