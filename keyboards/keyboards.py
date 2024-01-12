from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon_ru import (bot_commands, other_buttons, sex, edit_stop_or_not_buttons,
                                yes_no_buttons, edit_profile, edit_accept_buttons,
                                profile_assessment_buttons)


def set_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command=key, description=value)
        for key, value in bot_commands.items()
    ]
    return commands


def sex_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=value)]
        for value in sex.values()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def languages_keyboard(langs: list = None) -> InlineKeyboardMarkup:
    languages = [
        'Python', 'Ruby', 'C++', 'C#', 'C', 'Java', 'JavaScript',
        'Golang', 'Php', 'Assembler', 'Swift', 'Kotlin', 'Rust',
    ]
    if langs is not None:
        buttons = [
            [InlineKeyboardButton(text=lang, callback_data=f'set_language:{lang}')]
            for lang in languages if lang not in langs
        ]
        buttons.append([InlineKeyboardButton(text=other_buttons['next'], callback_data='next')])
    else:
        buttons = [
            [InlineKeyboardButton(text=lang, callback_data=f'set_language:{lang}')]
            for lang in languages
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def yes_no_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in yes_no_buttons.items()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def edit_profile_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in edit_profile.items()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def edit_accept_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in edit_accept_buttons.items()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def edit_stop_or_not_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in edit_stop_or_not_buttons.items()
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def profile_assessment_keyboard(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=f'{key}:{user_id}')]
        for key, value in list(profile_assessment_buttons.items())[:-1]
    ]
    message_button = [InlineKeyboardButton(
        text=profile_assessment_buttons['message'],
        url=f'tg://user?id={user_id}',
        callback_data='message'
    )]
    buttons.append(message_button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def profile_like_assessment(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=profile_assessment_buttons['dislike'],
                callback_data=f'dislike"{user_id}'
            )
        ],
        [
            InlineKeyboardButton(
                text=profile_assessment_buttons['message'],
                url=f'tg://user?id={user_id}',
                callback_data=f'message:{user_id}'
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
