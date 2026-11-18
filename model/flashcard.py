class Flashcard:

    # --- BOILERPLATE CODE ---
    # Setting variables from dictionary provided by the database
    
    def __init__(self, id, deck_id, english, mandarin, pinyin, times_reviewed=0, created_at=None):
        self.id = id
        self.deck_id = deck_id
        self.english = english
        self.mandarin = mandarin
        self.pinyin = pinyin
        self.times_reviewed = times_reviewed
        self.created_at = created_at

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        return cls(
            id=row["id"],
            deck_id=row["deck_id"],
            english=row["english"],
            mandarin=row["mandarin"],
            pinyin=row["pinyin"],
            times_reviewed=row["times_reviewed"],
            created_at=row["created_at"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "deck_id": self.deck_id,
            "english": self.english,
            "mandarin": self.mandarin,
            "pinyin": self.pinyin,
            "times_reviewed": self.times_reviewed,
            "created_at": self.created_at
        }


    # --- UTILITY METHODS FOR THE OBJECT ---
    def mark_reviewed(self):
        self.times_reviewed += 1
        with get_connection() as conn:
            conn.execute(
                "UPDATE flashcards SET times_reviewed = ? WHERE id = ?",
                (self.times_reviewed, self.id)
            )
            conn.commit()
    
    # --- UTILITY STATIC METHODS ---
    @classmethod
    def get_by_deck(cls, deck_id):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM flashcards WHERE deck_id = ?",
                (deck_id,)
            ).fetchall()
            cards = []
            for row in rows:
                cards.append(cls.from_row(row))
            return cards

    @classmethod
    def create(cls, deck_id, english, mandarin, pinyin):
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO flashcards (deck_id, english, mandarin, pinyin, times_reviewed)
                VALUES (?, ?, ?, ?, 0)
                """,
                (deck_id, english, mandarin, pinyin)
            )
            conn.commit()
            new_id = cursor.lastrowid
            row = conn.execute("SELECT * FROM flashcards WHERE id = ?", (new_id,)).fetchone()
            return cls.from_row(row)
