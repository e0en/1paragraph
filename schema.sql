CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE diary (
    user_id INTEGER REFERENCES user(id),
    day DATE KEY,
    title VARCHAR(64),
    content TEXT
);

CREATE UNIQUE INDEX diary_user_day ON diary (user_id, day);
