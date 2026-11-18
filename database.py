import sqlite3

DB_LOCALE = "flashcards.db"

def init_db():
    pass

# --- FUNCTIONS TO INTERACT WITH THE DATABASE ---

# Write (takes sql command)
def write_db(command: str, params: tuple = ()):
    with sqlite3.connect(DB_LOCALE) as conn:
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


# --- WRAP ALL THE SQL COMMANDS ---
def get_user_by_username(username: str):
    return read_db(
        "SELECT * FROM users WHERE username=?",
        (username,),
        fetch_all=False
    )

def get_user_decks(user_id: str):
    return read_db(
        "SELECT * FROM flashcard_decks WHERE user_id=? ORDER BY created_at DESC",
        (user_id,),
        fetch_all=True
    )




def get_all_cards():
    return read_db("SELECT * FROM cards")

def add_card(hanzi: str, py: str, meaning: str = ""):
    write_db(
        "INSERT INTO cards (hanzi, pinyin, meaning) VALUES (?, ?, ?)",
        (hanzi, py, meaning)
    )

def delete_card(card_id: int):
    write_db("DELETE FROM cards WHERE id = ?", (card_id,))
