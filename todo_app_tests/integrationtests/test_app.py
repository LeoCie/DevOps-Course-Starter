import os
import pytest
import requests
import mongomock
from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    addCardWithTitle(client, 'Test card')
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()

def addCardWithTitle(client, title):
    client.post('/add', data='title=' + title, follow_redirects=True,content_type='application/x-www-form-urlencoded')
 