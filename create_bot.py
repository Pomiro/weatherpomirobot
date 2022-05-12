from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import bot_token
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler_start = AsyncIOScheduler()
bot = Bot(token=bot_token)
dp = Dispatcher(bot)