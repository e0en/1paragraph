DROP TABLE IF EXISTS diarys;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE diarys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    day DATE,
    title VARCHAR(64),
    content TEXT
);

CREATE UNIQUE INDEX diary_user_day ON diarys (user_id, day);
