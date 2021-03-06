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
from keyboards import kb_cancel, kb_weather
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

scheduler = AsyncIOScheduler()  # run scheduler

connection = psycopg2.connect(  # connect to PostgreSQL
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    sslmode='require')

class FSMtimer(StatesGroup):
    start = State()
    weather = State()

class FSMNow(StatesGroup):
    start = State()
    weather = State()

# Weather Now
@dp.message_handler(lambda message: 'Погода сейчас' in message.text, state=None)
async def city_now(message: types.Message):
    await FSMNow.start.set()
    await FSMNow.next()
    await bot.send_message(message.from_user.id, "Введите название города")

@dp.message_handler(state=FSMNow.weather)
async def weather_now(message: types.Message, state: FSMNow):
    if len(requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}"  # check city
                        f"&limit=5&appid={open_weather_token}").json()) != 0:
        await bot.send_message(message.from_user.id, str(f"Погода в городе {message.text}:\n{get_weather(message.text)}"))
    else:
        await message.reply("🔴 Проверьте название города 🔴", reply_markup=kb_weather)
    await state.finish()

# Every morning weather
@dp.message_handler(lambda message: 'Погода каждое утро' in message.text, state=None)
async def get_city(message: types.Message):
    await FSMtimer.start.set()
    await FSMtimer.next()
    await bot.send_message(message.from_user.id, "Введите название города", reply_markup=kb_cancel)

@dp.message_handler(lambda message: 'Отмена отправки погоды' in message.text, state="*")
@dp.message_handler(Text(equals='Отмена отправки погоды', ignore_case=True,), state='*')
async def cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Прогноз погоды больше не будет приходить по утрам 😢",
                           reply_markup=kb_weather)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(f"DELETE from morning_weather where user_id={message.from_user.id}")
    cursor.close()
    await state.finish()

def get_weather(city):
    """
    When sending city, sends weather for 16 hours
    :param: city
    :return: final (string with weather)
    """
    code_to_smile = {  # emoji lib
        "Clear": "☀ Ясно",
        "Clouds": "☁ Облачно",
        "Rain": "☔ Дождь",
        "Drizzle": "☔ Дождь",
        "Thunderstorm": "⛈ Гроза",
        "Snow": "❄ Снег",
        "Mist": "🌫 Туман"
    }
    loc = requests.get(  # get request from server with city location
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={open_weather_token}"
    )
    loc = loc.json()   # read replay in json

    lat = loc[0]['lat']
    lon = loc[0]['lon']

    r = requests.get(  # get request from server with weather
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
    """
    Sends weather to user
    """
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, city from morning_weather")
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0],
        city = row[1],
        text = str(f"Погода в городе {city[0]}:\n{get_weather(city)}")
        await bot.send_message(chat_id=user_id[0], text=text)
    cursor.close()

scheduler.add_job(morning_push,
                  "cron",
                  hour=6,
                  minute=0,
                  start_date='2022-05-13 06:00:00',
                  timezone='Asia/Yekaterinburg',
                  )

@dp.message_handler(state=FSMtimer.weather)
async def get_query(message: types.Message, state: FSMContext):
    connection.autocommit = True
    cursor = connection.cursor()
    if len(requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}"  # check city
                        f"&limit=5&appid={open_weather_token}").json()) != 0:
        try:  # if it is new user, insert his data
            cursor.execute("INSERT INTO morning_weather VALUES (%s, %s)", (message.from_user.id, message.text))
        except:  # if it is not a new, update his data
            cursor.execute("UPDATE morning_weather set city = (%s) where user_id = (%s)",
                           (message.text, message.from_user.id))
        await bot.send_message(message.from_user.id, "Каждый день в 06:00 вам будет приходить прогноз погоды 🙂",
                               reply_markup=kb_weather)
    else:
        await message.reply("🔴 Проверьте название города 🔴")
    cursor.close()
    await state.finish()

async def on_startup(_):
    print('Bot online')

async def on_shutdown(_):
    print('Bot offline')
    connection.close()

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
