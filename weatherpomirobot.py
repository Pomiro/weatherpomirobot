from aiogram.utils import executor
from create_bot import dp, scheduler_start

async def on_startup(_):
	print('Bot online')

from handlers import base, scheduler, weather

if __name__ == '__main__':
	scheduler_start.start()
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)