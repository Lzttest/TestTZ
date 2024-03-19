import sqlite3

import data.config


class Database:

    def __init__(self, path=data.config.PATH_DATABASE):
        # Создаём и настраиваем подключения
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        # При первом запуске создаются таблицы
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
                )''')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                author TEXT NOT NULL,
                name TEXT NOT NULL,
                genre INTEGER,
                description TEXT NOT NULL,
                FOREIGN KEY (name) REFERENCES genres (id)
                )''')
        self.connection.commit()

    # Возвращает все сохранённые в БД книги
    def get_books(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM books').fetchall()

    # Сохранят книгу в БД
    def save_book(self, author: str, name: str, genre: int, description: str) -> int:
        with self.connection:
            self.cursor.execute("INSERT INTO books (author, name, genre, description) VALUES (?, ?, ?, ?)",
                                (author, name, genre, description))
            return self.cursor.lastrowid

    # Удаляет книгу с заданным айдишникмо
    def delete_book(self, book_id: int):
        with self.connection:
            self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))

    # Возвращает жанры книг
    def get_genres(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM genres").fetchall()

    # Сохраняет жанр в бд
    def save_genre(self, name: str) -> int:
        with self.connection:
            self.cursor.execute("INSERT INTO genres (name) VALUES (?)", (name,))
            return self.cursor.lastrowid
