from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import database
from lexicon.lexicon_ru import delete_profile
from keyboards.keyboards import yes_no_keyboard
from FSMS.FSMS import DeleteProfileSG


router = Router()


@router.message(Command('delete_profile'))
async def cmd_watch_profile(message: Message, state: FSMContext):
    profile = await database.check_user_in_database(message.from_user.id)
    if profile:
        await message.answer(
            text=delete_profile['delete'],
            reply_markup=yes_no_keyboard()
        )
        await state.set_state(DeleteProfileSG.accept_or_not_delete)
    else:
        await message.answer(
            text=delete_profile['delete_error']
        )


@router.callback_query(DeleteProfileSG.accept_or_not_delete, F.data == 'yes')
async def delete_profile_accept(callback: CallbackQuery, state: FSMContext):
    await database.edit_profile(
        user_id=callback.from_user.id,
        edit_parametr='watched_users',
        edit_value=str(callback.from_user.id),
        remove=True
    )
    await database.delete_profile(callback.from_user.id)
    await state.clear()
    await callback.message.edit_text(
        text=delete_profile['accept_delete']
    )


@router.callback_query(DeleteProfileSG.accept_or_not_delete, F.data == 'no')
async def delete_profile_accept(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=delete_profile['not_accept_delete']
    )
    await state.clear()
