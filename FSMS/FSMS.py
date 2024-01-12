from aiogram.fsm.state import State, StatesGroup


class RegistrationSG(StatesGroup):
    name = State()
    sex = State()
    age = State()
    city = State()
    languages = State()
    description = State()
    photo = State()


class EditProfileSG(StatesGroup):
    edit_menu = State()
    name = State()
    sex = State()
    age = State()
    city = State()
    languages = State()
    description = State()
    photo = State()
    save_or_not = State()


class DeleteProfileSG(StatesGroup):
    accept_or_not_delete = State()
