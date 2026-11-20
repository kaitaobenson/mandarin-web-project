import sqlite3
from contextlib import contextmanager
from typing import Iterator

DB_LOCALE = "flashcards.db"

def init_db():
    pass

# --- FUNCTIONS TO INTERACT WITH THE DATABASE ---

# Write (takes sql command)
def write_db(command: str, params: tuple = ()):
    with sqlite3.connect(DB_LOCALE) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        cursor = conn.cursor()
        cursor.execute(command, params)
        conn.commit()

# Read (takes sql command)
# Returns a list of dictionaries for each row in the database.
# [
#    {"id": 1, "hanzi": "你好", "pinyin": "nǐ hǎo", "meaning": "hello"},
#    {"id": 2, "hanzi": "谢谢", "pinyin": "xiè xie", "meaning": "thank you"}
# ]
def read_db(command: str, params: tuple = (), fetch_all: bool = True):
    with sqlite3.connect(DB_LOCALE) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(command, params)

        if fetch_all:
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        else:
            row = cursor.fetchone()
            if row:
                return (dict(row))
            else:
                return None

@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
  conn = sqlite3.connect(DB_LOCALE)
  # Crucial: allows dict(row) to work in from_row() and get_by_deck()
  conn.row_factory = sqlite3.Row
  # Optional but recommended: enforces foreign keys like deck_id
  

  try:
    with conn:  # Automatically commits on success, rolls back on exception
      yield conn
  finally:
    conn.close()  # Guarantees the file lock is released


# --- WRAP ALL THE SQL COMMANDS ---
