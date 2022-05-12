from create_bot import dp, bot, scheduler_start
from aiogram import types
from aiogram.dispatcher import Dispatcher

ID = None

async def test_message(dp : Dispatcher):
	await dp.bot.send_message(chat_id=ID, text="HI")

@dp.message_handler(commands=["timer"])
async def timer_command(message: types.Message):
	global ID
	ID = message.from_user.id
	await bot.send_message(message.from_user.id, "Я буду присылать сводку погоды каждое утро!")

def schedule_job():
	scheduler_start.add_job(test_message, "interval", seconds=5, args=(dp,))

schedule_job()