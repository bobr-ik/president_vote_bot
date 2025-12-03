from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.core import Base
from typing import Optional
from sqlalchemy import ForeignKey, String
from datetime import datetime, timedelta


class PhotosORM(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    poster_id: Mapped[int]
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    photo_id: Mapped[str]
    created_at: Mapped[datetime]

    user: Mapped["UsersORM"] = relationship("UsersORM", back_populates="photos")


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int]
    name: Mapped[str]
    completed_challenge: Mapped[bool] = mapped_column(default=False)
    got_present: Mapped[bool] = mapped_column(default=False)

    photos: Mapped[list[PhotosORM]] = relationship("PhotosORM", back_populates="user")
