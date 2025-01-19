CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    emailid TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    created_at DATE NOT NULL,
    updated_at DATE NOT NULL
);
