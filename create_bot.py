from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)