from aiogram.utils import executor
from create_bot import dp, scheduler_start

async def on_startup(_):
	await bot.set_webhook(config.URL_APP)
	print('Bot online')

async def on_shutdown(_):
	await bot.delete_webhook()

from handlers import base, scheduler, weather

if __name__ == '__main__':
	scheduler_start.start()
	#executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
	executor.start_webhook(
		dispatcher=dp,
		webhook_path='',
		on_startup=on_startup,
		on_shutdown=on_shutdown,
		skip_updates=True,
		host="0.0.0.0",
		port=5000
	)