DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS books;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  title TEXT  NOT NULL
  -- i want to make it so that the title does not need to be unique but so that the title and authro combo must be
);


-- In SQLite, data is stored in tables and columns.
-- These need to be created before you can store and retrieve data.
-- Flaskr will store users in the user table, and posts in the post table.
-- Create a file with the SQL commands needed to create empty tables:

