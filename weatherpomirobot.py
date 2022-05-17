import psycopg2
import requests
import datetime
from config import open_weather_token
from aiogram import types
from aiogram.utils import executor
from create_bot import dp, bot
from handlers import base
from config import db_name, db_user, db_password, db_host, db_port
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

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

async def morning_push():
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, city from morning_weather")
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0],
        city = row[1],
        text = str(f"Погода в городе {city[0]}:\n{get_weather(city)}")
        print(user_id[0])
        await bot.send_message(chat_id=user_id[0], text=text)
    cursor.close()

scheduler.add_job(morning_push,
                  "cron",
                  hour=6,
                  minute=0,
                  start_date='2022-05-13 06:00:00',
                  timezone='Asia/Yekaterinburg',
                  )

@dp.message_handler()
async def get_query(message: types.Message):
    connection.autocommit = True
    cursor = connection.cursor()
    if len(requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}"
                        f"&limit=5&appid={open_weather_token}").json()) != 0:
        try:
            cursor.execute("INSERT INTO morning_weather VALUES (%s, %s)", (message.from_user.id, message.text))
        except:
            cursor.execute("UPDATE morning_weather set city = (%s) where user_id = (%s)",
                           (message.text, message.from_user.id))
        await bot.send_message(message.from_user.id, "Каждый день в 06:00 вам будет приходить прогноз погоды 🙂")
    else:
        await message.reply("🔴 Проверьте название города 🔴")
    connection.commit()
    cursor.close()

async def on_startup(_):
    print('Bot online')

async def on_shutdown(_):
    print('Bot offline')
    connection.close()

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
