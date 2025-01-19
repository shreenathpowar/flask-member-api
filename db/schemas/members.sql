CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    emailid TEXT NOT NULL UNION,
    active INTEGER DEFAULT 1,
    mtype INTEGER NOT NULL,
    created_at DATE NOT NULL,
    updated_at DATE NOT NULL,
    FOREIGN KEY (mtype) REFERENCES memberships(id)
);
