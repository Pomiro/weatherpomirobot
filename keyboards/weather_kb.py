from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Город')

kb_weather = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_weather.row(b1)