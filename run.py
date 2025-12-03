from app import bot
import asyncio
from database import orm


if __name__ == "__main__":
    asyncio.run(orm.create_table())
    
    asyncio.run(bot.init_bot())