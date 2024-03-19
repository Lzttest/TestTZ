from aiogram import Dispatcher, Bot

from data.config import BOT_TOKEN
from library.library import Library

library = Library()
bot = Bot(BOT_TOKEN, parse_mode='html')
dp = Dispatcher()
