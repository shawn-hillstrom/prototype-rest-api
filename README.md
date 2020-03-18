# prototype-rest-api
A prototype REST API, by Shawn Hillstrom.

## Dependencies:

### Flask (v1.1.1)

**Install with**
```bash
pip install flask
```

### pytest (v5.4.1)

**Install with**
```bash 
pip install pytest
```

### sqlite3 (v3.28.0)

sqlite3 comes pre-installed on the latest versions of most Linux distros and Mac OS X.

## How To Use:

**Step 1.** Clone the repository.

**Step 2.** After the dependencies are installed you can run the set of unit tests I created with this application by running
```bash
pytest -rA
```

**Step 3.** To run individual unit tests run
```bash
pytest test_api.py::test_func_name
```

### List of Test Functions and Associated Unit Tests

- test_home
	1. Check to see if GET returns "Ok" (200).

- test_postQuestion
	1. Post a simple question and check to see if POST returns "Ok" (200).
	2. Post a duplicate question and check to see if POST returns "Conflict" (409).
	3. Post an incorrect question format and check to see if POST returns "Bad request" (400).

- test_getQuestion
	1. Check to see if the API returns an empty request response when empty.
	2. Check to see if the API can return a simple test question.
	3. Check to see if the API can return a simple test question based on a query.

- test_postResponse
	1. Post a response with an invalid question ID and check to see if POST returns "Not found" (404).
	2. Post a simple response and check to see if POST returns "Ok" (200).
	3. Post a duplicate response and check to see if POST returns "Conflict" (409).
	4. Post an incorrect response format and check to see if POST returns "Bad request" (400).

- test_getResponse
	1. Check to see if the API returns an empty request response when empty.
	2. Check to see if the API can return a simple response.
	3. Check to see if the API can return a simple test question based on a query involving the response ID.
	4. Check to see if the API can return a simple test question based on a query involving the referenced question ID.

- test_saveBookmark
	1. Post a bookmark with an invalid question ID and check to see if POST returns "Not found" (404).
	2. Post a bookmark with an invalid response ID and check to see if POST returns "Not found" (404).
	3. Post a bookmark to a simple question and check to see if POST returns "Ok" (200).
	4. Post a bookmark to a simple response and check to see if POST returns "Ok" (200).
	5. Post an incorrect bookmark format and check to see if POST returns "Bad request" (400).

- test_getBookmark
	1. Check to see if the API returns an empty request response when empty.
	2. Check to see if the API can return the correct data from a simple question stored in bookmarks.
	3. Check to see if the API can return the correct data from a simple response stored in bookmarks.

**NOTE:** When running individual test functions, all specified sub-tests will be run.

## API Specs:

**community/posts/questions**
- POST - create new question
- GET - view a question based on id or view all questions if no query is specified

**community/posts/responses**
- POST - create new response
- GET - view a set of responses given a response id or a question id, or all responses if no query is specified

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
		"type": "Type of post ('Questions' or 'Responses')",
		"id": "Unique ID for post",
		"user": "User who bookmarked the post"
	}
]
```
