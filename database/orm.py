from sqlalchemy import text, insert, select, or_, and_, BigInteger, cast, case, func, collate, delete, update
from database.core import async_engine, async_session_factory, Base
from database import models, core
from sqlalchemy.orm import selectinload, contains_eager, joinedload
from itertools import groupby
from datetime import datetime, timedelta



async def create_table():
    async_engine.echo = False
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_engine.echo = False   