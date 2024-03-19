# Возвращает клавиатуру главного меню
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data.config import STRINGS
from tg_bot import library_bot


# Возвращает клавиатуру главного меню
def main_menu_keyboard():
    buttons = [[KeyboardButton(text=STRINGS['ADD_NEW_BOOK_BUTTON']),
                KeyboardButton(text=STRINGS['LIST_BOOKS_BUTTON'])],
               [KeyboardButton(text=STRINGS['FIND_BY_GENRE_BUTTON']),
                KeyboardButton(text=STRINGS['FIND_BY_KEYWORD_BUTTON'])]]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return keyboard


# Возвращает клавиатуру с жанрами книг.
def genre_choice_keyboard():
    builder = ReplyKeyboardBuilder()

    genres = library_bot.library.genres_by_name.keys()
    # без жанров клавиатуру не создать
    if not genres:
        return None

    for genre in genres:
        builder.add(KeyboardButton(text=genre))

    return builder.as_markup(resize_keyboard=True)
