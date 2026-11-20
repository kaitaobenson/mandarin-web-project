from dataclasses import asdict, dataclass
import sqlite3
from typing import Self
from model.database import read_db, write_db


@dataclass
class Flashcard:
    id: int
    deck_id: int
    english: str
    mandarin: str
    pinyin: str
    times_reviewed: int = 0
    created_at: str | None = None

    @classmethod
    def from_row(cls, row: sqlite3.Row | None) -> Self | None:
        if row is None:
            return None
        
        # Unpacks the row directly into Flashcard(...) automatically!
        return cls(**dict(row))

    def to_dict(self) -> dict:
        return asdict(self)

    # --- DATABASE METHODS ---
    def edit_english(self, new_english: str) -> None:
        self.english = new_english

        write_db(
            "UPDATE flashcards SET english = ? WHERE id = ?",
            (self.english, self.id)
        )
    
    def edit_mandarin(self, new_mandarin: str) -> None:
        self.mandarin = new_mandarin
        write_db(
            "UPDATE flashcards SET mandarin = ? WHERE id = ?",
            (self.mandarin, self.id)
        )
    
    def edit_pinyin(self, new_pinyin: str) -> None:
        self.pinyin = new_pinyin
        write_db(
            "UPDATE flashcards SET pinyin = ? WHERE id = ?",
            (self.pinyin, self.id)
        )

    @classmethod
    def get_by_deck(cls, deck_id: int) -> list[Self]:
        rows = read_db(
            "SELECT * FROM flashcards WHERE deck_id = ?",
            (deck_id,),
            fetch_all=True
        )
        return [cls(**row) for row in rows]

    @classmethod
    def create(cls, deck_id: int, english: str, mandarin: str, pinyin: str) -> Self | None:
        new_id = write_db(
            """
            INSERT INTO flashcards (deck_id, english, mandarin, pinyin)
            VALUES (?, ?, ?, ?)
            """,
            (deck_id, english, mandarin, pinyin)
        )