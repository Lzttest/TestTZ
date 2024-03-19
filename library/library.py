from library.database import Database


class Genre:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Book:

    def __init__(self, book_id: int, author: str, name: str, genre: Genre, description: str):
        self.id = book_id
        self.author = author
        self.name = name
        self.genre = genre
        self.description = description

    # Проверяет вхождение строки в основные поля книги
    def __contains__(self, item: str):
        item = item.lower()
        return item in self.author.lower() or item in self.name.lower()


class Library:

    def __init__(self):
        self.bookshelf = dict()
        self.genres_by_name = dict()
        self.genres_by_id = dict()
        self.db = Database()
        self.load_data()

    def load_data(self):
        # загружаем информацию о жанрах
        for genre_data in self.db.get_genres():
            genre = Genre(genre_data['id'], genre_data['name'])
            self.genres_by_name[genre.name] = genre
            self.genres_by_id[genre.id] = genre
        # загружаем информацию о книгах
        for book_data in self.db.get_books():
            self.bookshelf[book_data['id']] = Book(book_data['id'], book_data['author'], book_data['name'],
                                                   self.genres_by_id[book_data['genre']], book_data['description'])

    def create_book(self, author: str, name: str, genre_name: str, description: str):
        # проверяем использовался ли жанр до этого, если нет записываем его в бд
        if genre_name not in self.genres_by_name:
            genre_id = self.db.save_genre(genre_name)
            genre = Genre(genre_id, genre_name)
            self.genres_by_id[genre_id] = genre
            self.genres_by_name[genre_name] = genre

        genre = self.genres_by_name[genre_name]
        book_id = self.db.save_book(author, name, genre.id, description)

        book = Book(book_id, author, name, genre, description)
        self.bookshelf[book_id] = book
        return book

    def remove_book(self, book_id: int):
        if book_id not in self.bookshelf:
            raise ValueError(f"Unknown book id: {book_id}")

        del self.bookshelf[book_id]
        self.db.delete_book(book_id)

    def get_book(self, book_id: int):
        # проверяем наличие книги в хранилище чтобы избежать ошибок
        if book_id not in self.bookshelf:
            return None
        return self.bookshelf[book_id]

    def get_books(self) -> list[Book]:
        # оборачиваем view на словарь в список
        return list(self.bookshelf.values())

    def get_genres(self) -> list[Genre]:
        return list(self.genres_by_name.values())

    def find_by_keyword(self, word: str) -> list[Book]:
        books = []
        for book in self.get_books():
            if word in book:
                books.append(book)
        return books

    def find_by_genre_name(self, genre_name: str) -> list[Book]:
        if genre_name not in self.genres_by_name:
            return []
        genre_id = self.genres_by_name[genre_name].id
        return self.find_by_genre_id(genre_id)

    def find_by_genre_id(self, genre_id: int) -> list[Book]:
        if genre_id not in self.genres_by_id:
            return []
        books = []
        # сравниваем данный жанр с жанром каждой книги, записываем результат в список
        for book in self.get_books():
            if book.genre.id == genre_id:
                books.append(book)
        return books
