from lib.db.connection import CONN, CURSOR
import sqlite3


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article id={self.id}, title='{self.title}'>"

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            )
        """)
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            """, (self.title, self.content, self.author_id, self.magazine_id))
            self.id = CURSOR.lastrowid
            CONN.commit()

    @classmethod
    def find_by_id(cls, article_id):
        CURSOR.execute("SELECT id, title, content, author_id, magazine_id FROM articles WHERE id = ?", (article_id,))
        row = CURSOR.fetchone()
        return cls(*row) if row else None

    def author(self):
        from lib.models.author import Author
        CURSOR.execute("SELECT id, name FROM authors WHERE id = ?", (self.author_id,))
        row = CURSOR.fetchone()
        return Author(*row) if row else None

    def magazine(self):
        from lib.models.magazine import Magazine
        CURSOR.execute("SELECT id, name, category FROM magazines WHERE id = ?", (self.magazine_id,))
        row = CURSOR.fetchone()
        return Magazine(*row) if row else None


