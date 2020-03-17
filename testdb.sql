/* Make sure existing tables are dropped */
DROP TABLE IF EXISTS Questions;
DROP TABLE IF EXISTS Responses;
DROP TABLE IF EXISTS Bookmarks;

/* Schema for questions table */
CREATE TABLE Questions (
	id			int,
	user		varchar(255),
	postdate	date,
	content		mediumtext,
	PRIMARY KEY (id)
);

/* Schema for responses table */
CREATE TABLE Responses (
	id			int,
	qid			int,
	user		varchar(255),
	postdate	date,
	content		mediumtext,
	PRIMARY KEY (id),
	FOREIGN KEY (qid) REFERENCES Questions(id)
);

/* Schema for bookmarks table */
CREATE TABLE Bookmarks (
	type		varchar(16),
	id			int,
	user		varchar(255)
);
