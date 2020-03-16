# Import dependencies
import os
import tempfile
import pytest
import json
from api import app, init_db

# Test data
question0 = { # Simple question set
	"id": 0,
	"user": "Bob",
	"postdate": "2020-02-28",
	"content": "Hello World!"
}
question1 = { # Incorrect question set
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
	response1 = client.post('/community/posts/questions', data=json.dumps(question0))
	assert response1.status_code == 200 # Ok

	# Sub-test 2: Post duplicate question
	response2 = client.post('/community/posts/questions', data=json.dumps(question0))
	assert response2.status_code == 409 # Conflict

	# Sub-test 3: Post incorrect format
	response3 = client.post('/community/posts/questions', data=json.dumps(question1))
	assert response3.status_code == 400 # Bad request

def test_getQuestion(client):
	''' Test case for getting questions. '''

	# Sub-test 1: Verify an empty returned list
	response1 = client.get('community/posts/questions')
	data1 = response1.get_json()
	assert len(data1) == 0

	# Sub-test 2: Get a simple question for a returned list
	client.post('/community/posts/questions', data=json.dumps(question0))
	response2 = client.get('community/posts/questions')
	data2 = response2.get_json()[0]
	assert 'id' in data2 and data2['id'] == question0['id']
	assert 'user' in data2 and data2['user'] == question0['user']
	assert 'postdate' in data2 and data2['postdate'] == question0['postdate']
	assert 'content' in data2 and data2['content'] == question0['content']

