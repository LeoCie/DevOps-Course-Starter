import os
import pytest
import requests
from todo_app import app
from threading import Thread
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    board_id = create_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    
    # construct the new application
    application = app.create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    
    # Tear Down
    thread.join(1)
    delete_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

trello_base_url = 'https://api.trello.com/1'
def create_board():
    board, authParams = loadEnvThenGetBoardAndAuthParams()

    board = requests.get(trello_base_url + f'/boards/{board}{authParams}')
    org_id = board.json()['idOrganization']

    create_response = requests.post(trello_base_url + f'/boards/{authParams}&name=e2e-Test-board&idOrganization={org_id}')
    if create_response.status_code != 200:
        raise Exception('Board could not be created')
    return create_response.json()['id']

def delete_board(board_id):
    board, authParams = loadEnvThenGetBoardAndAuthParams()
    delete_response = requests.delete(trello_base_url + f'/boards/{board_id}{authParams}')
    if delete_response.status_code != 200:
        raise Exception('Board could not be deleted')

def loadEnvThenGetBoardAndAuthParams():
    file_path = find_dotenv('.env')
    load_dotenv(file_path)
    board = os.getenv('TRELLO_BOARD_ID')
    token = os.getenv('TRELLO_TOKEN')
    key = os.getenv('TRELLO_KEY')
    authParams = f'?token={token}&key={key}'
    return board, authParams