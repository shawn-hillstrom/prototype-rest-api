# prototype-rest-api
Prototype REST API for Jetcake interview problem, by Shawn Hillstrom.

## Dependencies:
- Flask
- sqlite3
- jsonify (from Flask)
- request (from Flask)

## API Specs:

**community/posts/questions**
- POST - create new question
- GET - view all questions

**community/posts/responses**
- POST - create new response
- GET - view a set of responses given a question id or all responses if no query is specified

**community/posts/bookmarks**
- POST - create new bookmark
- GET - view all bookmarks

**NOTE:** PUT and DELETE would also be useful for questions and responses and DELETE would be useful for bookmarks, but these are not included here because they are not included in the problem parameters.

### Post questions for other users

**Definition**

'POST /community/posts/questions'

**Arguments**

- '"id":int' unique ID for post
- '"user":string' name of user who is posting
- '"postdate":string' date of post (YYYY-MM-DD)
- '"content":string' content of post

If a duplicate ID is received an error is returned.

### Post responses to questions

**Definition**

'POST /community/posts/responses'

**Arguments**

- '"id":int' ID of referenced question
- '"qid":int' ID of referenced question
- '"user":string' name of user who is posting
- '"postdate":string' date of post (YYYY-MM-DD)
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
		"postdate": "Date posted (YYYY-MM-DD)",
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
		"postdate": "Date posted (YYYY-MM-DD)",
		"content": "Body of the post"
	}
]
```

### Bookmark a post

**Definition**

'POST /community/posts/bookmarks'

**Arguments**

- '"type:string' type of post ("Questions" or "Responses")
- '"id":int' unique ID for post
- '"user":string' user who bookmarked the post

If the ID does not exist in the Questions database or the Responses database, an error is returned.

### View bookmarks

**Definition**

'GET /community/posts/bookmarks'

**Response**

```json
[
	{
		"type": "Type of post (\"question\" or \"response\")",
		"id": "Unique ID for post",
		"user": "User who bookmarked the post",
		"data": "JSON object containing the responses of either 'GET /community/posts/questions' or 'GET /community/posts/responses'"
	}
]
```
