-- FOR DEVELOPMENT ONLY
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS labels;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS purchases;

CREATE TABLE state (
    current__points REAL DEFAULT 0,
    total_points REAL DEFAULT 0,
    total_deep INTEGER DEFAULT 0,
    total_shallow INTEGER DEFAULT 0,
    deep_value REAL DEFAULT 1,
    shallow_value REAL DEFAULT 1,
    tdl_value REAL DEFAULT 1
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