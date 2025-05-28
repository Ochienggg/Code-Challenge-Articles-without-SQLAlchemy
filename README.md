
# 📰 Author-Magazine-Article Management System

A Python-based mini ORM project that models a publishing system with `Authors`, `Magazines`, and `Articles` using `sqlite3`. This project demonstrates fundamental object-relational mapping, database interaction, and modular architecture without using external frameworks.

---

## 📌 Overview

This system allows:

- Creating and managing **Authors**, **Magazines**, and **Articles**
- Associating articles with both authors and magazines
- Retrieving all articles by a specific author
- Finding all contributors (authors) to a particular magazine
- Running a fully persistent system using SQLite

---



## 🧱 Project Structure

```

your\_project/
│
├── main.py                        # Entry point to run the program
├── README.md                      # Project documentation
├── database.db                    # SQLite database file (auto-generated)
│
└── lib/
├── db/
│   └── connection.py          # Sets up SQLite connection and cursor
│
└── models/
├── author.py              # Author model and related methods
├── article.py             # Article model and relationships
└── magazine.py            # Magazine model and relationships

````

---

## 📦 Setup Instructions

### 1. Clone or Download the Project

```bash
git clone git@github.com:Ochienggg/Code-Challenge-Articles-without-SQLAlchemy.git
cd Code-Challenge-Articles-without-SQLAlchemy
````

### 2. Optional: Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Run the Application

```bash
python main.py
```

---

## 🧪 Example Workflow

Here's a sample of what the code usage looks like inside `main.py`:

```python
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

# Step 1: Create tables
Author.create_table()
Article.create_table()
Magazine.create_table()

# Step 2: Create and save entities
author = Author(name="Alice Johnson")
author.save()

magazine = Magazine(name="Science Weekly", category="Science")
magazine.save()

article = Article(
    id=None,
    title="The Future of Space Travel",
    content="Exploring Mars and beyond...",
    author_id=author.id,
    magazine_id=magazine.id
)
article.save()

# Step 3: Query relationships
print("Author's Articles:", author.articles())
print("Author's Magazines:", author.magazines())
print("Magazine's Articles:", magazine.articles())
print("Magazine's Contributors:", magazine.contributors())
```

---

## 🔍 Features in Detail

### Author Model (`author.py`)

* `create_table()`: Creates the authors table.
* `save()`: Inserts a new author into the database.
* `articles()`: Returns all articles written by this author.
* `magazines()`: Returns unique magazines this author has written for.

### Article Model (`article.py`)

* `create_table()`: Creates the articles table with foreign keys.
* `save()`: Inserts the article into the database.
* `find_by_id(id)`: Retrieves an article by ID.
* `author()`: Returns the `Author` of the article.
* `magazine()`: Returns the `Magazine` the article belongs to.

### Magazine Model (`magazine.py`)

* `create_table()`: Creates the magazines table.
* `save()`: Inserts or updates a magazine.
* `find_by_id(id)`: Retrieves a magazine by ID.
* `articles()`: Returns all articles published in the magazine.
* `contributors()`: Returns all distinct authors who contributed.

---

