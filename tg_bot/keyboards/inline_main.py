from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.config import STRINGS, BOOKS_PER_PAGE, GENRES_PER_PAGE
from library import Book
from tg_bot.library_bot import library


# Клавиатура для строго выбора жанра из списка.
def genre_strict_choice_keyboard(page: int):
    builder = InlineKeyboardBuilder()
    genres = library.get_genres()

    # если нет жанров клавиатуру сделать не получится
    if not genres:
        return None

    start_index = page * GENRES_PER_PAGE
    end_index = min(len(genres), (page + 1) * GENRES_PER_PAGE)

    # дополнительная защита от открытия нелегальных страниц
    if start_index > len(genres) - 1:
        return None

    for genre in genres[start_index:end_index]:
        builder.row(InlineKeyboardButton(text=genre.name, callback_data=f'genre_id_{genre.id}'))

    # если нам не хватило места для вывода всех жанров добавляем кнопки выбора страницы
    add_prev_page = page > 0  # если мы не на первой странице
    add_next_page = len(genres) > end_index  # если мы не на последней странице

    if add_prev_page or add_next_page:
        buttons = []
        if add_prev_page:
            buttons.append(
                InlineKeyboardButton(text=STRINGS['PREV_PAGE'], callback_data=f'list_genres_page_{page - 1}')
            )
        if add_next_page:
            buttons.append(
                InlineKeyboardButton(text=STRINGS['NEXT_PAGE'], callback_data=f'list_genres_page_{page + 1}')
            )
        builder.row(*buttons)

    return builder.as_markup(resize_keyboard=True)


# Микро клавиатура для удаления книг
def delete_book_keyboard(book_id: int):
    buttons = [[
        InlineKeyboardButton(text=STRINGS['DELETE_BOOK'], callback_data=f"delete_book_{book_id}")
    ]]

    return InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)


#  Возвращает клавиатуру для навигации по книгам из заданного списка
def list_books_keyboard(books: list[Book]):
    builder = InlineKeyboardBuilder()

    for book in books:
        text = (STRINGS['BOOK_SHORT_DESCRIPTION']
                .replace('%id%', str(book.id))
                .replace("%name%", book.name)
                .replace("%author%", book.author))
        builder.row(InlineKeyboardButton(text=text, callback_data=f'book_description_{book.id}'))

    return builder.as_markup(row_width=1, resize_keyboard=True)


#  Возвращает клавиатуру для навигации по книгам
def books_list_keyboard(page: int):
    books = library.get_books()
    # если книг в библиотеке нет не возвращаем ничего
    if not books:
        return None

    builder = InlineKeyboardBuilder()

    start_index = page * BOOKS_PER_PAGE
    end_index = min(len(books), (page + 1) * BOOKS_PER_PAGE)

    if start_index > len(books) - 1:
        return None

    for book in books[start_index:end_index]:
        text = (STRINGS['BOOK_SHORT_DESCRIPTION']
                .replace('%id%', str(book.id))
                .replace("%name%", book.name)
                .replace("%author%", book.author))
        builder.row(InlineKeyboardButton(text=text, callback_data=f'book_description_{book.id}'))

    # если нам не хватило места для вывода всех книг добавляем кнопки выбора страницы
    add_prev_page = page > 0 # если мы не на первой странице
    add_next_page = len(books) > end_index # если мы не на последней странице

    if add_prev_page or add_next_page:
        buttons = []
        if add_prev_page:
            buttons.append(InlineKeyboardButton(text=STRINGS['PREV_PAGE'], callback_data=f'list_books_page_{page - 1}'))
        if add_next_page:
            buttons.append(InlineKeyboardButton(text=STRINGS['NEXT_PAGE'], callback_data=f'list_books_page_{page + 1}'))
        builder.row(*buttons)

    return builder.as_markup(row_width=1, resize_keyboard=True)
