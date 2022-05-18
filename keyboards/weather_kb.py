from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Погода каждое утро')
b2 = KeyboardButton('Отмена отправки погоды')

kb_weather = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_weather.row(b1)
kb_cancel.row(b2)
