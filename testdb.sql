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
	id			int
);
