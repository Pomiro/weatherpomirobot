from aiogram.utils import executor
from create_bot import dp

async def on_startup(_):
	print('Bot online')

from handlers import base, weather, scheduler

weather.register_handlers_weather(dp)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
