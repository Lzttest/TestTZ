from aiogram import Dispatcher

from tg_bot.middlewares.admin_middleware import WhitelistMessageMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.message.middleware(WhitelistMessageMiddleware())
