from lib.db.connection import CONN, CURSOR
import sqlite3
from typing import Optional, List
import importlib


class Magazine:
    def __init__(self, name: str, category: str, id: Optional[int] = None):
        self.name = name
        self.category = category
        self.id = id

    def __repr__(self):
        return f"<Magazine id={self.id}, name='{self.name}', category='{self.category}'>"

    @classmethod
    def create_table(cls):
        """Create the magazines table if it doesn't exist."""
        try:
            CURSOR.execute("PRAGMA foreign_keys = ON;")
            CURSOR.execute("""
                CREATE TABLE IF NOT EXISTS magazines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            """)
            CONN.commit()
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Error creating magazines table: {e}") from e

    def save(self):
        """Insert or update the magazine record."""
        try:
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
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Error saving magazine: {e}") from e

    @classmethod
    def find_by_id(cls, magazine_id: int) -> Optional['Magazine']:
        """Retrieve a magazine by ID."""
        try:
            CURSOR.execute(
                "SELECT id, name, category FROM magazines WHERE id = ?",
                (magazine_id,)
            )
            row = CURSOR.fetchone()
            return cls(id=row[0], name=row[1], category=row[2]) if row else None
        except sqlite3.DatabaseError as e:
            raise RuntimeError(f"Error finding magazine by ID: {e}") from e

    def articles(self) -> List[object]:
        """Return a list of Article objects published in this magazine."""
        if self.id is None:
            raise ValueError("Magazine must be saved before retrieving articles.")

        try:
            if not hasattr(self, "_Article"):
                self._Article = importlib.import_module("lib.models.article").Article

            CURSOR.execute("""
                SELECT id, title, content, author_id, magazine_id
                FROM articles
                WHERE magazine_id = ?
            """, (self.id,))
            rows = CURSOR.fetchall()

            return [self._Article(*row) for row in rows]
        except (sqlite3.DatabaseError, ImportError, AttributeError) as e:
            raise RuntimeError(f"Error retrieving articles: {e}") from e

    def contributors(self) -> List[object]:
        """Return a list of distinct Author objects who contributed to this magazine."""
        if self.id is None:
            raise ValueError("Magazine must be saved before retrieving contributors.")

        try:
            if not hasattr(self, "_Author"):
                self._Author = importlib.import_module("lib.models.author").Author

            CURSOR.execute("""
                SELECT DISTINCT a.id, a.name
                FROM authors a
                JOIN articles art ON art.author_id = a.id
                WHERE art.magazine_id = ?
            """, (self.id,))
            rows = CURSOR.fetchall()

            return [self._Author(id=row[0], name=row[1]) for row in rows]
        except (sqlite3.DatabaseError, ImportError, AttributeError) as e:
            raise RuntimeError(f"Error retrieving contributors: {e}") from e





