from aiogram import Bot, Dispatcher
from config import settings
from .handlers import rt


async def init_bot():
    dp = Dispatcher()
    

    dp.include_router(rt)
    await dp.start_polling(settings.bot)
