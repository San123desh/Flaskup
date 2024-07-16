import sqlite3

conn = sqlite3.connect("books.sqlite")

cursor = conn.cursor()

sql_query = """CREATE TABLE IF NOT EXISTS `book` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    publication_year INTEGER NOT NULL
    )"""

cursor.execute(sql_query)
