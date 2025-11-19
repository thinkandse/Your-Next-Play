DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email   TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS playlist;
CREATE TABLE playlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_id TEXT NOT NULL,
    game_name TEXT NOT NULL,
    game_img TEXT,
    game_link TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
