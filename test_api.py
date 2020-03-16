# Import dependencies
import os
import tempfile
import pytest
import json
from api import app, init_db

# Test data
question0 = { # Simple question set
	"id": "0",
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

	# Define data sets
	dataSimple = {
		"id": "0",
		"user": "Bob",
		"postdate": "2020-02-28",
		"content": "Hello World!"
	}

	# Post simple data
	client.post('/community/posts/questions', data=json.dumps(dataSimple))

	response1 = client.get('community/posts/questions')
	assert response1.status_code == 200 #Ok

