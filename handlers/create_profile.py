from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from FSMS.FSMS import RegistrationSG
from lexicon.lexicon_ru import profile
from keyboards.keyboards import sex_keyboard, languages_keyboard
from database import database
from services.filters import CheckCity


router = Router()
create_states = []


@router.message(Command('create_profile'))
async def cmd_create_profile(message: Message, state: FSMContext):
    user = await database.check_user_in_database(message.from_user.id)
    if user:
        await message.answer(
            text=profile['create_profile_error'],
        )
    else:
        await state.set_state(RegistrationSG.name)
        await message.answer(
            text=profile['name']
        )


@router.message(RegistrationSG.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegistrationSG.sex)
    await message.answer(
        text=profile['sex'],
        reply_markup=sex_keyboard()
    )


@router.callback_query(RegistrationSG.sex)
async def set_sex(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sex=callback.data)
    await state.set_state(RegistrationSG.age)
    await callback.message.edit_text(
        text=profile['age']
    )


@router.message(RegistrationSG.age, F.text.isdigit())
async def set_correct_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await state.set_state(RegistrationSG.city)
    await message.answer(
        text=profile['city'],
    )


@router.message(RegistrationSG.age)
async def set_incorrect_age(message: Message):
    await message.answer(
        text=profile['incorrect_age']
    )


@router.message(RegistrationSG.city, CheckCity())
async def set_city_correct(message: Message, state: FSMContext):
    await state.update_data(city=message.text, languages=[])
    await state.set_state(RegistrationSG.languages)
    await message.answer(
        text=profile['set_first_languages'],
        reply_markup=languages_keyboard()
    )


@router.message(RegistrationSG.city)
async def set_city_incorrect(message: Message):
    await message.answer(
        text=profile['incorrect_city']
    )


@router.callback_query(RegistrationSG.languages, F.data.split(':')[0] == 'set_language')
async def set_languages(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    langs = data['languages']
    langs.append(callback.data.split(':')[-1])
    await state.update_data(languages=langs)
    await callback.message.edit_text(
        text=profile['set_other_languages'].format(', '.join(langs)),
        reply_markup=languages_keyboard(langs)
    )


@router.callback_query(RegistrationSG.languages, F.data == 'next')
async def set_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationSG.description)
    await callback.message.edit_text(
        text=profile['description']
    )


@router.message(RegistrationSG.description)
async def set_photo(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(RegistrationSG.photo)
    await message.answer(
        text=profile['photo']
    )


@router.message(RegistrationSG.photo, F.photo)
async def end_registration(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    profile_data = await state.get_data()
    await database.create_profile(message.from_user.id, profile_data)
    await state.clear()
    await message.answer(
        text=profile['end_registration']
    )


@router.message(RegistrationSG.photo)
async def end_registration(message: Message, state: FSMContext):
    await message.answer(
        text=profile['incorrect_photo']
    )
