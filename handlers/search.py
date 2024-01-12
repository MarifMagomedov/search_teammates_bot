from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.filters import Command
from lexicon.lexicon_ru import search
from database import database
from keyboards.keyboards import profile_assessment_keyboard, profile_like_assessment


router = Router()


@router.message(Command('search'))
async def cmd_search(message: Message):
    user = await database.check_user_in_database(message.from_user.id)
    if user:
        profile = await database.search_profile(message.from_user.id)
        if profile:
            profile[5] = ' 🏳️‍🌈 '.join(profile[5])
            await message.answer_photo(
                caption=search['profile'].format(*profile[1:]),
                photo=profile[-1],
                reply_markup=profile_assessment_keyboard(profile[0])
            )
        else:
            await message.answer(
                text=search['profiles_none']
            )
    else:
        await message.answer(
            text=search['search_error']
        )


@router.callback_query(F.data.split(':')[0].in_(['like', 'dislike']))
async def check_profile(callback: CallbackQuery, bot: Bot):
    data = callback.data.split(':')
    user_profile = list(await database.get_profile(callback.from_user.id))
    user_profile[5] = ' 🏳️‍🌈 '.join(user_profile[5])
    if data[0] == 'like':
        await bot.send_photo(
            chat_id=data[-1],
            photo=user_profile[-1],
            caption=search['profile_like'].format(*user_profile[1:]),
            reply_markup=profile_like_assessment(callback.from_user.id)
        )

    await database.edit_profile(callback.from_user.id, 'watched_users', data[-1])
    profile = await database.search_profile(callback.from_user.id)
    if not profile:
        await callback.message.answer(
            text=search['profiles_none']
        )
    else:
        profile[5] = ' 🏳️‍🌈 '.join(profile[5])
        zxc = InputMediaPhoto(
            media=profile[-1],
            caption=search['profile'].format(*profile[1:])
        )

        await callback.message.edit_media(
            media=zxc,
            reply_markup=profile_assessment_keyboard(profile[0])
        )
