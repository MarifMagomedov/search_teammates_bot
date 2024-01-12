from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import database
from FSMS.FSMS import EditProfileSG
from services.filters import CheckCity
from lexicon.lexicon_ru import commands, profile, edit_profile
from keyboards.keyboards import (sex_keyboard, edit_profile_menu, edit_stop_or_not_keyboard,
                                 languages_keyboard, edit_accept_keyboard)


router = Router()


@router.message(Command('edit_profile'))
async def cmd_edit_profile(message: Message, state: FSMContext):
    user = await database.check_user_in_database(message.from_user.id)
    if user:
        await state.set_state(EditProfileSG.edit_menu)
        await message.answer(
            text=commands['edit_profile_menu'],
            reply_markup=edit_profile_menu()
        )
    else:
        await message.answer(
            text=edit_profile['edit_error']
        )


# EDIT_NAME
@router.callback_query(EditProfileSG.edit_menu, F.data == 'name')
async def edit_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileSG.name)
    await callback.message.edit_text(
        text=profile['name']
    )


@router.message(EditProfileSG.name)
async def accept_or_not_edit_name(message: Message, state: FSMContext):
    await state.update_data(edit_value=message.text, edit_parametr='name')
    await state.set_state(EditProfileSG.save_or_not)
    await message.answer(
        text=commands['edit_accept_or_not'],
        reply_markup=edit_accept_keyboard()
    )


# EDIT SEX
@router.callback_query(EditProfileSG.edit_menu, F.data == 'sex')
async def edit_sex(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileSG.sex)
    await callback.message.edit_text(
        text=profile['sex'],
        reply_markup=sex_keyboard()
    )


@router.callback_query(EditProfileSG.sex)
async def accept_or_not_edit_sex(callback: Message, state: FSMContext):
    await state.update_data(edit_value=callback.data, edit_parametr='sex')
    await state.set_state(EditProfileSG.save_or_not)
    await callback.message.edit_text(
        text=commands['edit_accept_or_not'],
        reply_markup=edit_accept_keyboard()
    )


# EDIT AGE
@router.callback_query(EditProfileSG.edit_menu, F.data == 'age')
async def edit_age(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileSG.age)
    await callback.message.edit_text(
        text=profile['age']
    )


@router.message(EditProfileSG.age, F.text.isdigit())
async def accept_or_not_edit_age(message: Message, state: FSMContext):
    await state.update_data(edit_value=int(message.text), edit_parametr='age')
    await state.set_state(EditProfileSG.save_or_not)
    if 5 <= int(message.text) <= 100:
        await message.answer(
            text=commands['edit_accept_or_not'],
            reply_markup=edit_accept_keyboard()
        )
    else:
        await message.answer(
            text=profile['incorrect_age']
        )


@router.message(EditProfileSG.age)
async def incorrect_edit_age(message: Message):
    await message.answer(
        text=profile['incorrect_age'],
    )


# EDIT CITY
@router.callback_query(EditProfileSG.edit_menu, F.data == 'city')
async def edit_city(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileSG.city)
    await callback.message.edit_text(
        text=profile['city']
    )


@router.message(EditProfileSG.city, CheckCity())
async def accept_or_not_edit_city(message: Message, state: FSMContext):
    await state.update_data(edit_value=message.text, edit_parametr='city')
    await state.set_state(EditProfileSG.save_or_not)
    await message.answer(
        text=commands['edit_accept_or_not'],
        reply_markup=edit_accept_keyboard()
    )


@router.message(EditProfileSG.city)
async def incorrect_edit_age(message: Message):
    await message.answer(
        text=profile['incorrect_city'],
    )


# EDIT LANGUAGES
@router.callback_query(EditProfileSG.edit_menu, F.data == 'languages')
async def edit_languages(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileSG.languages)
    await state.update_data(edit_value=[], edit_parametr='languages')
    await callback.message.edit_text(
        text=profile['set_first_languages'],
        reply_markup=languages_keyboard()
    )


@router.callback_query(EditProfileSG.languages, F.data.split(':')[0] == 'set_language')
async def set_edit_languages(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    langs = data['edit_value']
    langs.append(callback.data.split(':')[-1])
    await state.update_data(edit_Value=langs)
    await callback.message.edit_text(
        text=profile['set_other_languages'].format(', '.join(langs)),
        reply_markup=languages_keyboard(langs)
    )


@router.callback_query(EditProfileSG.languages, F.data == 'next')
async def set_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileSG.save_or_not)
    await callback.message.edit_text(
        text=commands['edit_accept_or_not'],
        reply_markup=edit_accept_keyboard()
    )


# EDIT DESCRIPTION
@router.callback_query(EditProfileSG.edit_menu, F.data == 'description')
async def edit_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileSG.description)
    await callback.message.edit_text(
        text=profile['description']
    )


@router.message(EditProfileSG.description)
async def accept_or_not_edit_city(message: Message, state: FSMContext):
    await state.update_data(edit_value=message.text, edit_parametr='description')
    await state.set_state(EditProfileSG.save_or_not)
    await message.answer(
        text=commands['edit_accept_or_not'],
        reply_markup=edit_accept_keyboard()
    )


# EDIT PHOTO
@router.callback_query(EditProfileSG.edit_menu, F.data == 'photo')
async def edit_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditProfileSG.name)
    await callback.message.edit_text(
        text=profile['photo']
    )


@router.message(EditProfileSG.photo, F.photo)
async def accept_or_not_edit_city(message: Message, state: FSMContext):
    await state.update_data(edit_value=message.photo[-1].file_id, edit_parametr='photo')
    await state.set_state(EditProfileSG.save_or_not)
    await message.answer(
        text=commands['edit_accept_or_not'],
        reply_markup=edit_accept_keyboard()
    )


@router.message(EditProfileSG.photo)
async def incorrect_edit_age(message: Message):
    await message.answer(
        text=profile['incorrect_photo'],
    )


# SAVE, OT SAVE, BACK_TO_MENU
@router.callback_query(EditProfileSG.save_or_not, F.data == 'save')
async def accept_edit_name(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    edit_value = data['edit_value']
    edit_parametr = data['edit_parametr']
    await state.clear()
    await database.edit_profile(callback.from_user.id, edit_parametr, edit_value)
    await callback.message.edit_text(
        text=commands['edit_accept'],
        reply_markup=edit_stop_or_not_keyboard()
    )


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(EditProfileSG.edit_menu)
    await callback.message.edit_text(
        text=commands['edit_profile_menu'],
        reply_markup=edit_profile_menu()
    )


@router.callback_query(F.data == 'stop')
async def stop_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=commands['edit_stop']
    )
