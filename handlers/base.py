from create_bot import dp, bot
from aiogram import types
from keyboards import kb_weather

@dp.message_handler(commands=["start", "help"])
async def start_command(message: types.Message):
	await bot.send_message(message.from_user.id, "Привет! Я бот прогнозирующий погоду!", reply_markup=kb_weather)
	