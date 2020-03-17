# Import dependencies
import os
import tempfile
import pytest
import json
from api import app, init_db

# Test data
question0 = { # Simple question
	"id": 0,
	"user": "Bob",
	"postdate": "2020-02-28",
	"content": "Hello World!"
}
question1 = { # Incorrect question
	"incorrect": "field"
}
response0 = { # Simple response
	"id": 0,
	"qid": 0,
	"user": "Sally",
	"postdate": "2020-02-29",
	"content": "Hello Bob!"
}
response1 = { # Incorrect response
	"incorrect": "field"
}
bookmark0 = { # Simple question bookmark
	"type": "Questions",
	"id": 0,
	"user": "Bob"
}
bookmark1 = { # Simple response bookmark
	"type": "Responses",
	"id": 0,
	"user": "Bob"
}
bookmark2 = { # Incorrect bookmark
	"incorrect": "field"
}

@pytest.fixture
def client():
	''' pytest Fixture for Client
	:yield: a representation of client with a teporary database
	'''
	fd, app.config['DATABASE'] = tempfile.mkstemp()
	app.config['TESTING'] = True
	with app.test_client() as client:
		with app.app_context():
			init_db()
		yield client
	os.close(fd)
	os.unlink(app.config['DATABASE'])

def test_home(client):
	''' Test the blank home page.'''
	response = client.get('/')
	assert response.status_code == 200 # Ok

def test_postQuestion(client):
	''' Test cases for posting questions. '''

	# Sub-test 1: Post simple question
	test1 = client.post('/community/posts/questions', data=json.dumps(question0))
	assert test1.status_code == 200 # Ok

	# Sub-test 2: Post duplicate question id
	test2 = client.post('/community/posts/questions', data=json.dumps(question0))
	assert test2.status_code == 409 # Conflict

	# Sub-test 3: Post incorrect format
	test3 = client.post('/community/posts/questions', data=json.dumps(question1))
	assert test3.status_code == 400 # Bad request

def test_getQuestion(client):
	''' Test cases for getting questions. '''

	# Sub-test 1: Get empty response
	test1 = client.get('/community/posts/questions')
	data1 = test1.get_json()
	assert len(data1) == 0

	# Sub-test 2: Get simple question
	client.post('/community/posts/questions', data=json.dumps(question0))
	test2 = client.get('/community/posts/questions')
	data2 = test2.get_json()[0]
	assert 'id' in data2 and data2['id'] == question0['id']
	assert 'user' in data2 and data2['user'] == question0['user']
	assert 'postdate' in data2 and data2['postdate'] == question0['postdate']
	assert 'content' in data2 and data2['content'] == question0['content']

	# Sub-test 3: Get simple question based on id
	test3 = client.get('/community/posts/questions?id=0')
	data3 = test3.get_json()[0]
	assert 'id' in data3 and data3['id'] == question0['id']
	assert 'user' in data3 and data3['user'] == question0['user']
	assert 'postdate' in data3 and data3['postdate'] == question0['postdate']
	assert 'content' in data3 and data3['content'] == question0['content']

def test_postResponse(client):
	''' Test cases for posting responses. '''

	# Sub-test 1: Post response with invalid qid
	test1 = client.post('/community/posts/responses', data=json.dumps(response0))
	assert test1.status_code == 404 # Not found

	# Sub-test 2: Post simple response
	client.post('/community/posts/questions', data=json.dumps(question0))
	test2 = client.post('/community/posts/responses', data=json.dumps(response0))
	assert test2.status_code == 200 # Ok

	# Sub-test 3: Post duplicate response id
	test3 = client.post('/community/posts/responses', data=json.dumps(response0))
	assert test3.status_code == 409 # Conflict

	#Sub-test 4: Post incorrect format
	test4 = client.post('/community/posts/responses', data=json.dumps(response1))
	assert test4.status_code == 400 # Bad request

def test_getResponse(client):
	''' Test cases for posting responses. '''

	# Sub-test 1: Get empty response
	test1 = client.get('/community/posts/responses')
	data1 = test1.get_json()
	assert len(data1) == 0

	# Sub-test 2: Get simple response
	client.post('/community/posts/questions', data=json.dumps(question0))
	client.post('/community/posts/responses', data=json.dumps(response0))
	test2 = client.get('/community/posts/responses')
	data2 = test2.get_json()[0]
	assert 'id' in data2 and data2['id'] == response0['id']
	assert 'qid' in data2 and data2['qid'] == response0['qid']
	assert 'user' in data2 and data2['user'] == response0['user']
	assert 'postdate' in data2 and data2['postdate'] == response0['postdate']
	assert 'content' in data2 and data2['content'] == response0['content']

	# Sub-test 3: Get simple response with id
	test3 = client.get('/community/posts/responses?id=0')
	data3 = test3.get_json()[0]
	assert 'id' in data3 and data3['id'] == response0['id']
	assert 'qid' in data3 and data3['qid'] == response0['qid']
	assert 'user' in data3 and data3['user'] == response0['user']
	assert 'postdate' in data3 and data3['postdate'] == response0['postdate']
	assert 'content' in data3 and data3['content'] == response0['content']

	# Sub-test 4: Get simple response with question id
	test4 = client.get('/community/posts/responses?qid=0')
	data4 = test4.get_json()[0]
	assert 'id' in data4 and data4['id'] == response0['id']
	assert 'qid' in data4 and data4['qid'] == response0['qid']
	assert 'user' in data4 and data4['user'] == response0['user']
	assert 'postdate' in data4 and data4['postdate'] == response0['postdate']
	assert 'content' in data4 and data4['content'] == response0['content']

def test_saveBookmark(client):
	''' Test cases for saving bookmarks. '''

	# Sub-test 1: Save question with invalid id
	test1 = client.post('/community/posts/bookmarks', data=json.dumps(bookmark0))
	assert test1.status_code == 404 # Not found

	# Sub-test 2: Save response with invalid id
	test2 = client.post('/community/posts/bookmarks', data=json.dumps(bookmark1))
	assert test2.status_code == 404 # Not found

	# Sub-test 3: Save simple question
	client.post('/community/posts/questions', data=json.dumps(question0))
	test3 = client.post('/community/posts/bookmarks', data=json.dumps(bookmark0))
	assert test3.status_code == 200 # Ok

	# Sub-test 4: Save simple response
	client.post('/community/posts/responses', data=json.dumps(response0))
	test4 = client.post('/community/posts/bookmarks', data=json.dumps(bookmark1))
	assert test4.status_code == 200 # Ok

	# Sub-test 5: Save incorrect format
	test5 = client.post('/community/posts/bookmarks', data=json.dumps(bookmark2))
	assert test5.status_code == 400 # Bad request

def test_getBookmark(client):
	''' Test cases for getting bookmarks. '''

	# Sub-test 1: Get empty response
	test1 = client.get('/community/posts/bookmarks')
	data1 = test1.get_json()
	assert len(data1) == 0

	# Sub-test 2: Get simple question from bookmarks
	client.post('/community/posts/questions', data=json.dumps(question0))
	client.post('/community/posts/bookmarks', data=json.dumps(bookmark0))
	test2 = client.get('/community/posts/bookmarks')
	data2 = test2.get_json()[0]
	assert 'type' in data2 and data2['type'] == bookmark0['type']
	assert 'id' in data2 and data2['id'] == bookmark0['id']
	assert 'user' in data2 and data2['user'] == bookmark0['user']
	subtest2 = client.get('/community/posts/questions?id=%i' % data2['id'])
	subdata2 = subtest2.get_json()[0]
	assert 'id' in subdata2 and subdata2['id'] == question0['id']
	assert 'user' in subdata2 and subdata2['user'] == question0['user']
	assert 'postdate' in subdata2 and subdata2['postdate'] == question0['postdate']
	assert 'content' in subdata2 and subdata2['content'] == question0['content']

	# Sub-test 3: Get simple response from bookmarks
	client.post('/community/posts/responses', data=json.dumps(response0))
	client.post('/community/posts/bookmarks', data=json.dumps(bookmark1))
	test3 = client.get('/community/posts/bookmarks')
	data3 = test3.get_json()[1]
	assert 'type' in data3 and data3['type'] == bookmark1['type']
	assert 'id' in data3 and data3['id'] == bookmark1['id']
	assert 'user' in data3 and data3['user'] == bookmark1['user']
	subtest3 = client.get('/community/posts/responses?id=%i' % data3['id'])
	subdata3 = subtest3.get_json()[0]
	assert 'id' in subdata3 and subdata3['id'] == response0['id']
	assert 'qid' in subdata3 and subdata3['qid'] == response0['qid']
	assert 'user' in subdata3 and subdata3['user'] == response0['user']
	assert 'postdate' in subdata3 and subdata3['postdate'] == response0['postdate']
	assert 'content' in subdata3 and subdata3['content'] == response0['content']

