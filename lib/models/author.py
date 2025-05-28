from lib.db.connection import CONN, CURSOR

class Author:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    @classmethod
    def create_table(cls):
        """Create the authors table if it doesn't exist."""
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        CONN.commit()

    def save(self):
        """Insert the author into the database and assign its ID."""
        CURSOR.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
        self.id = CURSOR.lastrowid
        CONN.commit()

    def articles(self):
        """Return a list of Article objects written by this author."""
        if self.id is None:
            raise ValueError("Author must be saved before retrieving articles.")
        from lib.models.article import Article
        CURSOR.execute("""
            SELECT id, title, content, author_id, magazine_id 
            FROM articles 
            WHERE author_id = ?
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [Article(row[1], row[2], row[3], row[4], id=row[0]) for row in rows]

    def magazines(self):
        """Return a list of distinct Magazine objects associated with this author."""
        if self.id is None:
            raise ValueError("Author must be saved before retrieving magazines.")
        from lib.models.magazine import Magazine
        CURSOR.execute("""
            SELECT DISTINCT m.id, m.name, m.category 
            FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [Magazine(row[1], row[2], id=row[0]) for row in rows]


    