from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import bot_token

bot = Bot(token=bot_token)
dp = Dispatcher(bot)