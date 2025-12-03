from aiogram.types import InputMediaPhoto
from collections import defaultdict
from .models import Photo


def group_photos(photos):
    media = defaultdict(list)
    for i, photo in enumerate(photos):
        photo: Photo
        media[photo.tg_id] += [
            InputMediaPhoto(
                media=photo.photo_id,
                caption=f'{photo.name} ({photo.tg_id})' if i == 0 else None  # caption только у первого
            )
        ]
    
    return media


def format_photo_for_user(photos: list[Photo], caption=None):
    media = []
    for i, photo in enumerate(photos):
        photo: Photo
        media += [
            InputMediaPhoto(
                media=photo.photo_id,
                caption=caption if i == 0 else None  # caption только у первого
            )
        ]
    
    return media
    