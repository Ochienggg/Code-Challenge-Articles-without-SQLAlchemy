from lib.db.connection import CONN, CURSOR

class Article:
    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = id

    def save(self):
        CURSOR.execute("""
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        """, (self.title, self.content, self.author_id, self.magazine_id))
        self.id = CURSOR.lastrowid
        CONN.commit()