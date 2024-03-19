from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from data.config import STRINGS
from tg_bot.keyboards.inline_main import books_list_keyboard, delete_book_keyboard, list_books_keyboard, \
    genre_strict_choice_keyboard
from tg_bot.keyboards.reply_main import main_menu_keyboard, genre_choice_keyboard
from tg_bot.library_bot import dp, bot, library


class AddBook(StatesGroup):
    choosing_book_name = State()
    choosing_book_genre = State()
    choosing_book_description = State()
    choosing_book_author = State()


class SearchByGenre(StatesGroup):
    choosing_book_genre = State()


class SearchByKeyword(StatesGroup):
    choosing_keyword = State()


@dp.message(
    Command(commands=["start"]),
)
async def cmd_start(message: Message):
    await message.reply(text=STRINGS['BOT_DESCRIPTION'], reply_markup=main_menu_keyboard())


# ДОБАВЛЕНИЕ КНИГИ
@dp.message(F.text == STRINGS['ADD_NEW_BOOK_BUTTON'])
async def add_new_book(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text=STRINGS['REQUEST_BOOK_NAME'])
    await state.set_state(AddBook.choosing_book_name)


@dp.message(AddBook.choosing_book_name)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_name=message.text)

    keyboard = genre_choice_keyboard()
    if keyboard:
        await bot.send_message(message.from_user.id, text=STRINGS['REQUEST_CHOICE_BOOK_GENRE'],
                               reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, text=STRINGS['REQUEST_BOOK_GENRE'])
    await state.set_state(AddBook.choosing_book_genre)


@dp.message(AddBook.choosing_book_genre)
async def genre_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_genre=message.text)

    await bot.send_message(message.from_user.id, text=STRINGS['REQUEST_BOOK_DESCRIPTION'])
    await state.set_state(AddBook.choosing_book_description)


@dp.message(AddBook.choosing_book_description)
async def description_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_description=message.text)

    await bot.send_message(message.from_user.id, text=STRINGS['REQUEST_BOOK_AUTHOR'])
    await state.set_state(AddBook.choosing_book_author)


@dp.message(AddBook.choosing_book_author)
async def author_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_author=message.text)

    book_data = await state.get_data()

    library.create_book(book_data['chosen_author'],
                        book_data['chosen_name'],
                        book_data['chosen_genre'],
                        book_data['chosen_description'])

    await bot.send_message(message.from_user.id, text=STRINGS['BOOK_ADDED'], reply_markup=main_menu_keyboard())
    await state.clear()


# КОНЕЦ ДОБАВЛЕНИЯ КНИГИ


# НАЧАЛО ВЫВОДА СПИСКА КНИГ
@dp.message(F.text == STRINGS['LIST_BOOKS_BUTTON'])
async def list_books(message: Message, state: FSMContext):
    keyboard = books_list_keyboard(0)
    if keyboard is None:
        await bot.send_message(message.from_user.id, STRINGS['LIBRARY_EMPTY'])
        return

    await bot.send_message(message.from_user.id, STRINGS['BOOKS_LIST'], reply_markup=keyboard)


@dp.callback_query(F.data.startswith('book_description_'))
async def book_description(callback: CallbackQuery):
    await callback.answer()
    book_id = int(callback.data.replace('book_description_', ''))
    book = library.get_book(book_id)
    text = (STRINGS['BOOK_GREATER_DESCRIPTION']
            .replace('%id%', str(book.id))
            .replace("%name%", book.name)
            .replace("%author%", book.author)
            .replace("%description%", book.description))

    await bot.send_message(callback.from_user.id, text=text, reply_markup=delete_book_keyboard(book_id))


@dp.callback_query(F.data.startswith("list_books_page_"))
async def list_books(callback: CallbackQuery):
    await callback.answer()
    page = int(callback.data.replace('list_books_page_', ''))
    if page < 0:
        return

    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text=STRINGS['BOOKS_LIST'], reply_markup=books_list_keyboard(page))
# КОНЕЦ ВЫВОДА СПИСКА КНИГ


# Удаление книги
@dp.callback_query(F.data.startswith('delete_book_'))
async def delete_book(callback: CallbackQuery):
    await callback.answer()
    book_id = int(callback.data.replace('delete_book_', ''))
    book = library.get_book(book_id)
    if book is None:
        return

    library.remove_book(book_id)
    await bot.send_message(callback.from_user.id, text=STRINGS['BOOK_DELETED'])


# Поиск книг по жанру
@dp.message(F.text == STRINGS['FIND_BY_GENRE_BUTTON'])
async def find_books_by_genre(message: Message, state: FSMContext):
    keyboard = genre_strict_choice_keyboard(0)
    if keyboard:
        await bot.send_message(message.from_user.id, text=STRINGS['CHOICE_BOOK_GENRE'],
                               reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, text=STRINGS['LIBRARY_EMPTY'])
        return

    await state.set_state(SearchByGenre.choosing_book_genre)


@dp.callback_query(SearchByGenre.choosing_book_genre, F.data.startswith('list_genres_page_'))
async def genres_choose_page(callback: CallbackQuery):
    page = int(callback.data.replace('list_genres_page_', ''))

    if page < 0:
        return

    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text=STRINGS['CHOICE_BOOK_GENRE'], reply_markup=books_list_keyboard(page))


@dp.message(SearchByGenre.choosing_book_genre)
async def genre_chosen(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text=STRINGS['SEARCHING'], reply_markup=main_menu_keyboard())
    await state.clear()

    books = library.find_by_genre_name(message.text)
    if not books:
        await bot.send_message(message.from_user.id, text=STRINGS['NO_BOOKS_FOUND'])
        return

    keyboard = list_books_keyboard(books)
    await bot.send_message(message.from_user.id, text=STRINGS['BOOKS_FOUND'], reply_markup=keyboard)


# Конец поиска книг по жанру.


# Поиск книг по ключевому слову.
@dp.message(F.text == STRINGS['FIND_BY_KEYWORD_BUTTON'])
async def find_books_by_keyword(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, STRINGS['REQUEST_SEARCH_QUERY'])
    await state.set_state(SearchByKeyword.choosing_keyword)


@dp.message(SearchByKeyword.choosing_keyword)
async def keyword_chosen(message: Message):
    books = library.find_by_keyword(message.text)

    if not books:
        await bot.send_message(message.from_user.id, text=STRINGS['NO_BOOKS_FOUND'])
        return

    keyboard = list_books_keyboard(books)
    await bot.send_message(message.from_user.id, text=STRINGS['BOOKS_FOUND'], reply_markup=keyboard)
# Конец поиска книг по ключевому слову.
