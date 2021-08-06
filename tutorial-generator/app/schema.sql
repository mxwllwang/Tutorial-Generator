DROP TABLE IF EXISTS tg;

CREATE TABLE tg (
  id INT PRIMARY KEY, 
  error TEXT NOT NULL,
  tutorial TEXT
);

INSERT INTO tg (id, error, tutorial)
VALUES (1, 'My Error', 'My Tutorial');

INSERT INTO tg (id, error, tutorial)
VALUES (2, 'My Error 2', 'My Tutorial 2');

/* Don't do bulk insert for now. */