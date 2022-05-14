from create_bot import dp, bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
#from apscheduler.schedulers.asyncio import AsyncIOScheduler

# scheduler_start = AsyncIOScheduler()

# ID = None

# async def test_message(dp : Dispatcher):
# 	await dp.bot.send_message(chat_id=ID, text="HI")

# @dp.message_handler(commands=["timer"])
# async def timer_command(message: types.Message):
# 	global ID
# 	ID = message.from_user.id
# 	await bot.send_message(message.from_user.id, "Ведите название города")
# 	@dp.message_handler()
# def schedule_job():
# 	scheduler_start.add_job(test_message, 'cron', hour=6, timezone='Asia/Yekaterinburg', start_date=datetime.now(), args=(dp,))
# 	# scheduler_start.add_job(test_message, "interval",seconds=5, 
# 	# 												#start_date='2022-05-13 06:00:00',
# 	# 												timezone='Asia/Yekaterinburg', 
# 	# 												args=(dp,))
# schedule_job()

