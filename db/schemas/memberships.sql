CREATE TABLE memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    adds_level INTEGER NOT NULL,
    streaming_quality TEXT NOT NULL,
    max_devices INTEGER NOT NULL,
    active INTEGER DEFAULT 1,
    created_at DATE NOT NULL,
    updated_at DATE NOT NULL
);
