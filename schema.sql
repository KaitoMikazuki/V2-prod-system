-- FOR DEVELOPMENT ONLY
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS labels;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS purchases;

CREATE TABLE state (
    current__points REAL,
    total_points REAL DEFAULT 0,
    total_deep INTEGER,
    total_shallow INTEGER,
    deep_value REAL DEFAULT 1,
    shallow_value REAL DEFAULT 1,
    tdl_value REAL DEFAULT 1
    mode TEXT 
        DEFAULT 'game'
        CHECK(mode IN ('game', 'track'))
);

CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    work_type TEXT CHECK(work_type IN('deep','shallow')),
    minutes INTEGER,
    seconds INTEGER,
    logged_at TEXT DEFAULT(datetime('now')),
    points REAL,
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