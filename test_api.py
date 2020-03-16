import pytest

from api import app

@pytest.fixture
def client():
	app.config['TESTING'] = True
	with app.test_client() as client:
		yield client

def test_home(client):
	''' Test the blank home page.'''
	response = client.get('/')
	assert response.status_code == 200, "Invalid get status" # 200 = get success
