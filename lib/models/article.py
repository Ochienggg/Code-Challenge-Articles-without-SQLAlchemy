from lib.db.connection import CONN, CURSOR

class Article:
    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = id

    @classmethod
    def create_table(cls):
        """Create the articles table if it doesn't exist."""
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                FOREIGN KEY(author_id) REFERENCES authors(id),
                FOREIGN KEY(magazine_id) REFERENCES magazines(id)
            )
        """)
        CONN.commit()

    def save(self):
        """Insert or update the article in the database."""
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                (self.title, self.content, self.author_id, self.magazine_id)
            )
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute(
                "UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.content, self.author_id, self.magazine_id, self.id)
            )
        CONN.commit()

    def delete(self):
        """Delete the article from the database."""
        if self.id is None:
            raise ValueError("Article must be saved before it can be deleted.")
        CURSOR.execute("DELETE FROM articles WHERE id = ?", (self.id,))
        CONN.commit()
        self.id = None
