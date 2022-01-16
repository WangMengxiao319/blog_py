-- 创建posts表

DROP TABLE IF EXISTS posts;
CREATE TABLE posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP,'localtime')),
    title TEXT NOT NULL,
    content TEXT NOT NULL
);