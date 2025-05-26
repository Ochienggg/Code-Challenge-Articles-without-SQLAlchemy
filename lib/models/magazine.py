from lib.db.connection import CURSOR, CONN


class Magazine:
    def __init__(self, name, category, id=None):
        self.name = name
        self.category = category
        self.id = id

    def save(self):
        CURSOR.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
        self.id = CURSOR.lastrowid
        CONN.commit()

    def articles(self):
        from lib.models.article import Article
        CURSOR.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = CURSOR.fetchall()
        return [Article(row[1], row[2], row[3], row[4], id=row[0]) for row in rows]

    def contributors(self):
        from lib.models.author import Author
        CURSOR.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles art ON art.author_id = a.id
            WHERE art.magazine_id = ?
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(row[1], id=row[0]) for row in rows]