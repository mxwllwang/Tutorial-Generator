DROP TABLE IF EXISTS tg;

CREATE TABLE tg (
  id INT, error TEXT NOT NULL, tutorial TEXT,
  PRIMARY KEY (id)
);

INSERT INTO tg (id, error, tutorial)
VALUES (1, 'My Error', 'My Tutorial')

INSERT INTO tg (id, error, tutorial)
VALUES (2, 'My Error 2', 'My Tutorial 2')

/* Don't do bulk insert for now. */


/*
DROP TABLE IF EXISTS err;
DROP TABLE IF EXISTS tg;

CREATE TABLE err (
  id INT, msg TEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE tg (
  id INT, tutorial TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id) REFERENCES user (id)
);
*/