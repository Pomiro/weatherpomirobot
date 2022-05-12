from create_bot import dp, bot
from aiogram import types

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
	await bot.send_message(message.from_user.id, "Привет! Напиши мне название города и я пришлю сводку погоды!")