-- FOR DEVELOPMENT ONLY
DROP TABLE state;
DROP TABLE logs;
DROP TABLE labels;
DROP TABLE items;
DROP TABLE purchases;

CREATE TABLE state (
    total_points REAL DEFAULT 0,
    current__points REAL,
    mode TEXT 
        DEFAULT 'game'
        CHECK(mode IN ('game', 'track'))
);

CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    work_type TEXT CHECK(work_type IN('deep','shallow')),
    minutes INTEGER CHECK(minutes >= 0),
    seconds INTEGER CHECK(seconds >= 0),
    logged_at TEXT DEFAULT(datetime('now')),
    day INTEGER CHECK(day >= 1 AND day <= 31),
    month INTEGER CHECK(month >= 1 AND month <= 12),
    year INTEGER,
    label TEXT DEFAULT NULL,
    notes TEXT DEFAULT NULL
);

CREATE TABLE labels (
    id INTEGER PRIMARY KEY,
    label TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    item TEXT,
    price INTEGER
);

CREATE TABLE purchases (
    id INTEGER PRIMARY KEY,
    purchase TEXT,
    logged_at TEXT DEFAULT(datetime('now')),
    price INTEGER
);