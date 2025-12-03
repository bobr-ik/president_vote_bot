from sqlalchemy import text, insert, select, or_, and_, BigInteger, cast, case, func, collate, delete, update
from database.core import async_engine, async_session_factory, with_db_session
from database import models, core
from sqlalchemy.orm import selectinload, contains_eager, joinedload
from itertools import groupby
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app import models as m


@with_db_session
async def check_user_exists(session: AsyncSession, user_id: int, username: str):
    stmt = select(models.UsersORM).where(models.UsersORM.tg_id == user_id)

    user = await session.execute(stmt)
    user = user.scalars().first()

    if not user:
        user = models.UsersORM(tg_id=user_id, name=username)
        session.add(user)

        await session.commit()

    return user



@with_db_session
async def check_if_already_loaded(session: AsyncSession, user_id, poster_id, username):
    await check_user_exists(user_id, username)

    stmt = select(models.PhotosORM).where(
        models.PhotosORM.tg_id == user_id,
        models.PhotosORM.poster_id == poster_id
    )

    photo = await session.execute(stmt)
    photo = photo.scalars().first()

    if photo:
        return True

    return False


@with_db_session
async def get_how_much_photos(session: AsyncSession, user_id):
    stmt = select(func.count(models.PhotosORM.id)).where(models.PhotosORM.tg_id == user_id)

    ans = await session.execute(stmt)
    ans = ans.scalar()

    return ans



@with_db_session
async def save_photo(session: AsyncSession, user_id, photo_id, poster_id):
    stmt = delete(models.PhotosORM).where(models.PhotosORM.tg_id == user_id, models.PhotosORM.poster_id == poster_id)

    await session.execute(stmt)

    photo = models.PhotosORM(
        tg_id=user_id,
        photo_id=photo_id,
        poster_id=poster_id,
        created_at=datetime.now()
    )
    session.add(photo)

    await session.commit()


@with_db_session
async def get_all_photos(session: AsyncSession):
    stmt = (
        select(
            models.PhotosORM.tg_id,
            models.PhotosORM.poster_id,
            models.PhotosORM.photo_id,
            models.UsersORM.name
        )
        .join(models.UsersORM, models.PhotosORM.tg_id == models.UsersORM.tg_id)
        .order_by(models.UsersORM.name)
    )

    photos = await session.execute(stmt)
    photos = photos.all()

    print(photos)
    return list(map(m.Photo.model_validate, photos))


@with_db_session
async def get_all_photos_by_user(session: AsyncSession, tg_id: int):
    stmt = (
        select(
            models.PhotosORM.tg_id,
            models.PhotosORM.poster_id,
            models.PhotosORM.photo_id,
            models.UsersORM.name
        )
        .join(models.UsersORM, models.PhotosORM.tg_id == models.UsersORM.tg_id)
        .where(models.PhotosORM.tg_id == tg_id)
        .order_by(models.UsersORM.name)
    )

    photos = await session.execute(stmt)
    photos = photos.all()

    print(photos)
    return list(map(m.Photo.model_validate, photos)) if photos else None
