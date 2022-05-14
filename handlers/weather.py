from create_bot import dp, bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from config import open_weather_token
from keyboards import kb_weather

import datetime
import requests

async def get_city(message : types.Message):
	await bot.send_message(message.from_user.id, "Введите название города")

async def get_weather(message : types.Message):
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

	try:
		# Отправка запроса на сервер для получение координат города
		loc = requests.get(
			f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&limit=5&appid={open_weather_token}"
		)
		loc = loc.json()

		lat = loc[0]['lat']
		lon = loc[0]['lon']

		r = requests.get(
			f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily&appid={open_weather_token}&units=metric&lang=ru"
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
		await message.reply(final)
	except:
		await message.reply("🔴 Проверьте название города 🔴")

def register_handlers_weather(dp : Dispatcher):
	dp.register_message_handler(get_city, lambda message: 'Город' in message.text)
	dp.register_message_handler(get_weather)