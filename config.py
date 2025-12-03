from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from aiogram import Bot

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    bot_token: str
    admin_id: list[int]

    @property
    def bot(self):
        return Bot(token=self.bot_token)
    

    @property
    def db_url(self):
        return f"sqlite+aiosqlite:///{BASE_DIR}/database/database.db"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
    

settings = Settings()