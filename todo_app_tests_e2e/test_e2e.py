import os
from selenium.webdriver.firefox.options import Options
import pytest
import pymongo
from todo_app import app
from threading import Thread
from selenium import webdriver
from dotenv import load_dotenv, find_dotenv

@pytest.fixture(scope='module')
def app_with_temp_db():
    # Create the new db & update the mongo db name environment variable
    setTestEnvVariables()

    # construct the new application
    application = app.create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    
    # Tear Down
    thread.join(1)
    drop_db()

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.headless = True
    with webdriver.Firefox(options=opts) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_db):
    driver.get('http://127.0.0.1:5000/')
    assert driver.title == 'To-Do App'

def setTestEnvVariables():
    file_path = find_dotenv('.env')
    load_dotenv(file_path)
    os.environ['MONGO_DB_NAME'] = 'items-e2e-test'
    os.environ['LOGIN_DISABLED'] = 'True'
    
def drop_db():
    connection_string = os.getenv('MONGO_DB_CONNECTION_STRING')
    client = pymongo.MongoClient(connection_string)
    client.drop_database(os.getenv('MONGO_DB_NAME'))
