from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from database import database
from lexicon.lexicon_ru import commands, watch_profile


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text=commands['start']
    )


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        text=commands['help']
    )


@router.message(Command('watch_profile'))
async def cmd_watch_profile(message: Message):

    result = await database.check_user_in_database(message.from_user.id)
    if not result:
        await message.answer(
            text=watch_profile['watch_error']
        )
    else:
        profile = await database.get_profile(message.from_user.id)
        profile = list(profile)
        profile[5] = ' 🏳️‍🌈 '.join(profile[5])
        await message.answer_photo(
            caption=watch_profile['watch'].format(*profile[1:]),
            photo=profile[-1]
        )
