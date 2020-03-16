# prototype-rest-api
Prototype REST API for Jetcake interview problem, by Shawn Hillstrom.

## Dependencies:
- Flask
- sqlite3
- jsonify (from Flask)
- request (from Flask)

## API Specs:

**community/post/questions**
- GET - view a subset of questions or all questions if no query is specified
- POST - create new question

**community/post/responses**
- GET - view a subset of responses or all responses if no query is specified
- POST - create new response

**community/bookmarks**
- GET - view a subset of bookmarks or all bookmarks if no query is specified

**NOTE:** PUT and DELETE would also be useful for questions and responses, but are not included here because they are not included in the specifications.

### Post questions for other users

**Definition**

'POST /community/posts/questions'

**Arguments**

- '"id":int' unique ID for post
- '"user":string' name of user who is posting
- '"date":string' date of post (YYYY-MM-DD)
- '"content":string' content of post

If a duplicate ID is received an error is returned.

### Post responses to questions

**Definition**

'POST /community/posts/responses'

**Arguments**

- '"id":int' ID of referenced question
- '"qid":int' ID of referenced question
- '"user":string' name of user who is posting
- '"date":string' date of post (YYYY-MM-DD)
- '"content":string' content of post

If a duplicate ID is received an error is returned.

### View questions

**Definition**

'GET /community/posts/questions'

**Response**

- '200' on success

```json
[
	{
		"id": "Unique ID for post",
		"user": "Name of user who posted",
		"date": "Date posted (YYYY-MM-DD)",
		"content": "Body of the post"
	}
]
```

### View responses

**Definition**

'GET /community/posts/responses'

**Response**

- '200' on success

```json
[
	{
		"id": "Unique ID for post",
		"qid": "ID of referenced question",
		"user": "Name of user who posted",
		"date": "Date posted (YYYY-MM-DD)",
		"content": "Body of the post"
	}
]
```

### Bookmark a post

**Definition**

'POST /community/posts/bookmarks'

**Arguments**

- '"type:string' type of post ("question" or "response")
- '"id":int' unique ID for post

If a duplicate ID is received an error is returned.

### View bookmarks

**Definition**

'GET /community/posts/bookmarks'

**Response**

```json
[
	{
		"type": "Type of post (\"question\" or \"response\")",
		"id": "Unique ID for post",
		"data": "JSON object containing the responses of either 'GET /community/posts/questions' or 'GET /community/posts/responses'"
	}
]
```
