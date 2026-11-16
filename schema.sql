PRAGMA foreign_keys = ON;

CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	-- Login info
	username TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE,
	password_hash TEXT NOT NULL,
	-- Account details
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL
);

CREATE TABLE flashcard_decks(
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	-- Deck details 
	name TEXT NOT NULL
);

CREATE TABLE flashcards (
	id INTEGER PRIMARY KEY,
	deck_id INTEGER REFERENCES flashcard_decks(id) ON DELETE CASCADE,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	-- Card details
	english TEXT,
	mandarin TEXT,
	pinyin TEXT,
	-- Card stats
	times_reviewed INTEGER NOT NULL
);


