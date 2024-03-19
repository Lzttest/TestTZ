import asyncio

from tg_bot.library_bot import bot
from tg_bot.handlers import dp
from tg_bot.middlewares import setup_middlewares


async def main():
    setup_middlewares(dp)

    print('Starting Telegram bot...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
