from lib.db.connection import CONN, CURSOR
import sqlite3


class Author:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"<Author id={self.id}, name='{self.name}'>"

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = CURSOR.lastrowid
            CONN.commit()

    def articles(self):
        if self.id is None:
            raise ValueError("Author must be saved before retrieving articles.")
        from lib.models.article import Article
        CURSOR.execute("""
            SELECT id, title, content, author_id, magazine_id 
            FROM articles 
            WHERE author_id = ?
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [Article(*row) for row in rows]

    def magazines(self):
        if self



    