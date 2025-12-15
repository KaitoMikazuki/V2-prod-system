-- DECIMALS ALWAYS HAVE TWO DECIMAL. 
-- DECIMALS ARE STORED AS INTEGERS WHICH ARE SCALED

-- FOR DEVELOPMENT ONLY
DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS labels;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS purchases;

CREATE TABLE state (
    current_points INTEGER DEFAULT 0, -- decimal
    total_points INTEGER DEFAULT 0, -- decimal
    total_deep INTEGER DEFAULT 0, -- decimal
    total_tdl INTEGER DEFAULT 0, -- decimal
    total_shallow INTEGER DEFAULT 0, -- decimal
    deep_value INTEGER DEFAULT 200, -- decimal
    shallow_value INTEGER DEFAULT 100, -- decimal
    tdl_value INTEGER DEFAULT 400 -- decimal
);

CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    work_type TEXT CHECK(work_type IN('deep','shallow', 'tdl')),
    minutes INTEGER,
    seconds INTEGER,
    logged_at TEXT DEFAULT(datetime('now')),
    points INTEGER, -- decimal
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