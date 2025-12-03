from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class ChangePhoto(CallbackData, prefix='change_photo'):
    poster_id: int


async def wanna_change_photo(poster_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да', callback_data=ChangePhoto(poster_id=poster_id).pack()),
                InlineKeyboardButton(text='Нет', callback_data='back')
            ]
        ]
    )


more = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Узнать подробнее', callback_data='more')
        ]
    ]
)