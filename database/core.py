from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import String, event
from config import settings
from typing import Annotated

# асинхронный движоек
async_engine = create_async_engine(
    url=settings.db_url,
    echo=True,  # выключение логов
    pool_size=5,
    max_overflow=10,
    connect_args={"check_same_thread": False}
)

# Дополнительная настройка через event
@event.listens_for(async_engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA encoding = 'UTF-8'")
    cursor.execute("PRAGMA case_sensitive_like = ON")
    cursor.close()

# как бы исполнитель запросов
async_session_factory = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# дополнительный класс данных для бд
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    # добавляем аннотации
    type_annotation_map = {
        str_256: String(256),
    }

    repr_columns_num = 200
    repr_cols = tuple()

    def __repr__(self):  # переделка принта моделей в логах
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_columns_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"{self.__class__.__name__}({', '.join(cols)})"

def with_db_session(func):
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            res = await func(session, *args, **kwargs)
        return res
    return wrapper