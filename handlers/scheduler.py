import time
import schedule
from multiprocessing.context import Process
from aiogram import Dispatcher
from aiogram import types
from create_bot import bot
#from handlers.weather import get_weather

async def get_base_city(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите название города")
    #global city
    city = message.text
    #schedule.every().seconds(3).do(get_weather)
#    schedule.every().day.at("08:00").do(get_weather)

class ScheduleMessage():
    def try_send_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_process(self):
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(get_base_city, lambda message: 'Погода каждое утро' in message.text)