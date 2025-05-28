from lib.db.connection import CONN, CURSOR

class Magazine:
    def __init__(self, name, category, id=None):
        self.name = name
        self.category = category
        self.id = id

    @classmethod
    def create_table(cls):
        """Create the magazines table if it doesn't exist."""
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)
        CONN.commit()

    def save(self):
        """Insert a new magazine or update an existing one."""
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )
        CONN.commit()

    def articles(self):
        """Return a list of Article objects published in this magazine."""
        if self.id is None:
            raise ValueError("Magazine must be saved before retrieving articles.")

        from lib.models.article import Article  # Import here to avoid circular imports

        CURSOR.execute("""
            SELECT id, title, content, author_id, magazine_id
            FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        rows = CURSOR.fetchall()

        return [Article(row[1], row[2], row[3], row[4], id=row[0]) for row in rows]

    def contributors(self):
        """Return a list of distinct Author objects who have contributed to this magazine."""
        if self.id is None:
            raise ValueError("Magazine must be saved before retrieving contributors.")

        from lib.models.author import Author  # Import here to avoid circular imports

        CURSOR.execute("""
            SELECT DISTINCT a.id, a.name
            FROM authors a
            JOIN articles art ON art.author_id = a.id
            WHERE art.magazine_id = ?
        """, (self.id,))
        rows = CURSOR.fetchall()

        return [Author(row[1], id=row[0]) for row in rows]



