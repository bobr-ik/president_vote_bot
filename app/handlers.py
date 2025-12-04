from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.filters import CommandStart, Command
from config import settings
from app import crud, patterns as p, keyboards as kb, functions as fu


rt = Router()


class LoadPhoto(StatesGroup):
    load_photo = State()


@rt.message(CommandStart(deep_link=True))
async def with_deep_link(message: Message, command: Command, state: FSMContext):
    await message.delete()

    poster_id = int(decode_payload(command.args).replace('poster_', ''))
    if await crud.check_if_already_loaded(message.from_user.id, poster_id, message.from_user.username):
        await message.answer(p.already_loaded, reply_markup=await kb.wanna_change_photo(poster_id))
    else:
        how_much_photos = await crud.get_how_much_photos(message.from_user.id)

        await message.answer(p.need_to_load.format(how_much_photos=str(how_much_photos).rjust(2, ' ')), reply_markup=kb.more)
        await state.set_state(LoadPhoto.load_photo)
        await state.update_data(poster_id=poster_id)


@rt.callback_query(kb.ChangePhoto.filter())
async def change_photo(callback: CallbackQuery, callback_data: kb.ChangePhoto, state: FSMContext):
    await callback.answer()

    poster_id = callback_data.poster_id

    how_much_photos = await crud.get_how_much_photos(callback.from_user.id)

    await callback.message.edit_text(p.need_to_load.format(how_much_photos=str(how_much_photos).rjust(2, ' ')), reply_markup=kb.more)
    await state.set_state(LoadPhoto.load_photo)
    await state.update_data(poster_id=poster_id)


@rt.message(LoadPhoto.load_photo, F.photo)
async def load_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    poster_id = await state.get_value('poster_id')

    await crud.save_photo(message.from_user.id, photo, poster_id)

    how_much_photos = await crud.get_how_much_photos(message.from_user.id)
    if how_much_photos == 10:
        await message.answer(p.congrats, reply_markup=kb.more)
    else:
        await message.answer(p.saved.format(how_much_photos=str(how_much_photos).rjust(2, ' ')), reply_markup=kb.more)

    
@rt.callback_query(F.data == 'more')
async def more(callback: CallbackQuery):
    await callback.answer()
    photos = await crud.get_all_photos_by_user(callback.from_user.id)

    if not photos:
        await callback.message.edit_text(p.no_photos.format(how_much_photos=0))
        return
    media = fu.format_photo_for_user(photos, p.more.format(how_much_photos=len(photos)))

    await settings.bot.send_media_group(
        chat_id=callback.from_user.id, 
        media=media
    )


# @rt.message(F.photo)
# async def save_photo_file_id(message: Message):
#     photo_id = message.photo[-1]

    


# @rt.message()
# async def echo(message: Message):
#     text = ''
#     for i in range(10):
#         referral_link = await create_start_link(
#             bot=settings.bot,
#             payload=f"poster_{i}",
#             encode=True  # Кодировать payload (рекомендуется)
#         )
#         text += f"{referral_link}\n"

#     await message.answer(text)


@rt.message(lambda message: message.from_user.id in settings.admin_id and message.text == '/admin')
async def show_all_photos_by_user(message: Message):
    photos = await crud.get_all_photos()

    media = fu.group_photos(photos)

    for user_id, photos in media.items():
        await settings.bot.send_media_group(
            chat_id=message.from_user.id, 
            media=photos
        )

    # await message.answer_photo()