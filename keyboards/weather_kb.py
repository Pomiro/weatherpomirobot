from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Погода каждое утро')

kb_weather = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_weather.row(b1)
