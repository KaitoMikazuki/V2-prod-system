-- FOR DEVELOPMENT ONLY
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS labels;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS purchases;

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
    minutes INTEGER CHECK(minutes > 0),
    seconds INTEGER CHECK(seconds >= 0),
    logged_at TEXT DEFAULT(datetime('now')),
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