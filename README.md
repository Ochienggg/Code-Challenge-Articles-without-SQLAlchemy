# Python OOP Project: Authors, Articles & Magazines

This project demonstrates a simple Object-Oriented Programming (OOP) design in Python with persistent storage using SQLite. It models a basic publishing system with `Author`, `Article`, and `Magazine` classes.

---

## Features

- Define authors who write articles.
- Articles belong to magazines.
- Authors can have multiple articles.
- Magazines have multiple articles and contributors.
- Basic CRUD operations with SQLite database.
- Demonstrates relationships between models using SQL JOIN queries.

---

## Project Structure

```

lib/
├── db/
│   ├── connection.py       # Database connection and cursor
├── models/
│   ├── author.py           # Author class
│   ├── article.py          # Article class
│   ├── magazine.py         # Magazine class
├── testing/
│   ├── author\_test.py      # Tests for Author
│   ├── article\_test.py     # Tests for Article
│   ├── magazine\_test.py    # Tests for Magazine

````

---

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/Ochienggg/Code-Challenge-Articles-without-SQLAlchemy.git
cd your-repo-name
````

2. **Install dependencies**

This project uses the standard library, so no extra dependencies are required.

3. **Initialize the database**

Make sure you have a SQLite database set up with tables: `authors`, `articles`, `magazines`.

Example SQL schema:

```sql
CREATE TABLE authors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE magazines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  category TEXT NOT NULL
);

CREATE TABLE articles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  author_id INTEGER NOT NULL,
  magazine_id INTEGER NOT NULL,
  FOREIGN KEY(author_id) REFERENCES authors(id),
  FOREIGN KEY(magazine_id) REFERENCES magazines(id)
);
```

---

## Usage

* Create and save Authors, Articles, and Magazines.
* Query related objects, e.g., get all articles by an author or all contributors to a magazine.

Example:

```python
from lib.models.author import Author

author = Author("Jane Doe")
author.save()

articles = author.articles()
for article in articles:
    print(article.title)
```

---

## Testing

Tests are written using `pytest`.

Run tests with:

```bash
pytest
```

---

## Contributing

Feel free to submit issues or pull requests.

---
