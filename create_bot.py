from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


bot = Bot(token = '5595760542:AAE7pdeCacTGRCJGlbAVWSjwzyyrrMujQo8')
dp = Dispatcher(bot, storage = storage)
